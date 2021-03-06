#!/usr/bin/env python3
import re
import os

from web import exceptions


class GenBank:
    """
    This class handles the interactions pretaining to the genbank file.
    It's also responsible for creating the chromosome and gene objects.
    The data from the genbank file is stored in 1 large string, so this
    script is non streaming. We opted for this option because we thought
    the code would more flexible this way.
    """

    def __init__(self, content=None, filename=None):
        """
        file_string:        The string containing the entire genbank file.
        chromosome:         The chromosome object for the genbank file.
        genes:              A list of gene objects for the chromosome
        :param content:        The path + filename for the genbank file one wishes to excecute.
        """
        self.file_string = str()

        if content is not None:
            self.file_string = content
            self.filename = filename
        elif filename is not None:
            self.file = filename
            self._read_file()

        self.chromosome = None
        self.genes = None

    def __str__(self):
        return self.file_string

    def _read_file(self):
        """
        This method is only calleble by the class itself.
        It opens the genbank file for the current path + filename
        and sets the file_string for the current genbank file.
        """
        handle = open(self.file, 'r')
        var = handle.readlines()
        self.file_string = ''.join(var)
        handle.close()

    def make_chromosome(self):
        """
        This method handles the creation of the chromosome object.
        It accomplishes this using regex.

        :return: A chromosome object.
        """

        # The regex code that searches for the chromosome.
        definition = re.search('DEFINITION\s*(.*)\schromosome\s(\w+)', self.file_string)

        if definition:
            definition = definition
        else:
            # If  mitochondrion is present.
            definition = re.search('DEFINITION\s*(.*)\s(mitochondrion)', self.file_string)

            if definition is None:
                raise exceptions.ParseException()

        organism = definition.group(1).replace(",", "")
        chromosome_id = definition.group(2)

        seq = re.search('ORIGIN(.*)//', self.file_string, re.DOTALL)

        if seq is None:
            raise exceptions.ParseException()

        seq = seq.group(1)
        seq = re.sub('\n|\s|\d', '', seq).lower()

        self.chromosome = Chromosome(seq, chromosome_id, organism)

        return self.chromosome

    def make_genes(self):
        """
        This method handles the creation of the gene objects.
        :return: A list of gene objects.
        """

        # The regex to get all of the coding DNA seqeunces.
        cds_info = re.findall('CDS(.+?)/translation', self.file_string, re.DOTALL)
        if len(cds_info) < 1:
            raise exceptions.ParseException('No genes found in the genbank file: ')

        # Creates the dict for the creation of an reverse complement.
        trans_table = str.maketrans("atcg", "tagc")
        gene_list = list()
        strand = str()

        for cur_cds in cds_info:

            # The regex to get all of the info from an cds.
            exon_seqs = list()

            exon_regions = re.findall('.(\d+)\.\.>?(\d+)', cur_cds, re.DOTALL)
            gene_id = re.search('/db_xref="GI:(\d*)', cur_cds)
            protein_id = re.search('/protein_id="(.*)"', cur_cds)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL)

            if not all([exon_regions, gene_id, protein_id, protein_name]):
                raise exceptions.ParseException()

            gene_id = gene_id.group(1)
            protein_id = protein_id.group(1)
            protein_name = protein_name.group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)

            for i, exon in enumerate(exon_regions):

                # If a strand is a complement excecute this.
                if re.match('.*complement', cur_cds):
                    strand = '-'
                    gen_seq = self.chromosome.seq[int(exon[0]):int(exon[1])][::-1]  # Reverse the strand.
                    gen_seq = gen_seq.translate(trans_table)  # Make the stand complement.
                    exon_seqs.append(gen_seq)

                else:
                    strand = '+'
                    gen_seq = self.chromosome.seq[int(exon[0])-1:int(exon[1])-1]  # Get the strand
                    exon_seqs.append(gen_seq)

            # Create the seqeunce string for the gene.
            if strand == '-':
                exon_seqs = ''.join(exon_seqs[::-1])  # If the strand is negative it needs to be joined in reverse

            elif strand == '+':
                exon_seqs = ''.join(exon_seqs)  # Join the strands normally

            # Creation of the gene objects.
            gene_list.append(Gene(gene_id,
                                  strand,
                                  exon_regions,
                                  exon_seqs,
                                  protein_name,
                                  protein_id,
                                  self.chromosome))

        self.genes = gene_list

        return self.genes


class Chromosome:
    """
    The class that servers as a framework to store the chromosome
    data.
    """

    def __init__(self, seq, chromosome_def, organism):

        # TODO add a var to store the db id
        self.chromosome_id = chromosome_def
        self.database_id = int()
        self.seq = seq
        self.organism = organism
        self.organism_id = None
        self.genes = list()


class Gene:
    """
    The class that servers as a framework to store the gene
    data.
    """

    def __init__(self, gene_id, strand, exon_regions, exon_seqs, protein, protein_id, chromosome):

        self.gene_id = gene_id
        self.chromosome_id = chromosome.chromosome_id
        self.organism = chromosome.organism
        self.strand = strand
        self.exon_regions = exon_regions
        self.exon_seqs = exon_seqs
        self.protein = protein
        self.protein_id = protein_id
        self.probes = list()

        self.database_id = int()

        self.possible_probe_count = 0
        self.probe_count = 0
        self.mono_count = 0
        self.di_count = 0
        self.hairpin_count = 0
        self.gc_count = 0

        self.time_total = 0
        self.time_mono = 0
        self.time_di = 0
        self.time_hairpin = 0
        self.time_gc = 0


class FastaWriter:
    """
    The class that handles the creation of the fasta files.
    """

    @staticmethod
    def get_gene_string(genes):
        """
        This method creates the gene fasta file
        :param genes: A list of Gene objects
        """

        # The creation of the filename .
        gene_list = list()
        filename = ('Genes_chromosome-' + genes[0].chromosome_id
                    + '_' + genes[0].organism.replace(' ', '-'))

        for gene in genes:

            # Creation of the fasta id.
            gen_seq = gene.exon_seqs
            seq_to_write = list()

            seq_to_write.append('>gene_'
                                + str(gene.gene_id)
                                + '|' + str(gene.strand)
                                + '|' + str(gene.protein).replace(' ', '-') + '\n')

            for i in range(0, len(gen_seq), 75):
                seq_to_write.append(gen_seq[i:i+75] + '\n')

            gene_list.append(''.join(seq_to_write) + '\n\n')

        return [''.join(gene_list), filename]

    @staticmethod
    def get_chromosome_string(chromosome):

        filename = ('Chromosome-' + str(chromosome.chromosome_id)
                    + '_' + str(chromosome.organism.replace(' ', '-')))

        # Creation of the fasta id.
        fasta_id = '>chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism) + '\n'

        # Add a newline char every 75 chars
        seq_to_write = []
        for i in range(0, len(chromosome.seq), 75):
            seq_to_write.append(chromosome.seq[i:i+75])

        file_string = fasta_id + '\n'.join(seq_to_write)

        return [file_string, filename]

    @staticmethod
    def get_probe_string(genes, prober):

        # The creation of the filename .
        probe_list = list()
        filename = 'Probes_' + str(1) + '_' + genes[0].organism.replace(' ', '-') + '_chromosome-' + str(genes[0].chromosome_id) + '.fa'
        # filename = 'Probes_test.fa'

        for gene in genes:

            seq_to_write = list()
            for probe in gene.probes:

                seq_to_write.append('>'
                                    + str(probe.probe_id)
                                    + '\n')
                seq_to_write.append(probe.sequence + '\n\n')

            probe_list.append(''.join(seq_to_write))

        return [''.join(probe_list), filename]

    def write_probes_gondor(self, probe_list, file_count, output_dir=''):

        probe_count = len(probe_list)
        probes_per_file = int((probe_count / file_count))

        i = 0
        file_number = 1
        probes_in_current_file = 0

        seq_to_write = list()
        for probe in probe_list:

            seq_to_write.append('>'
                                + str(probe.probe_id)
                                + '\n')
            seq_to_write.append(probe.sequence + '\n\n')

            probes_in_current_file += 1

            if probes_in_current_file == probes_per_file:

                filename = 'probes_' + str(file_number)
                if os.path.exists(output_dir+filename):
                    duplicate_file_iter = 1

                    while os.path.exists(output_dir+filename+'({0})'.format(str(duplicate_file_iter))):
                        duplicate_file_iter += 1

                    print('[WARNING] File: ',
                          filename,
                          ' Exists.\n\t Created: ',
                          filename, '({0}) instead'.format(str(duplicate_file_iter)))

                    filename += '({0})'.format(str(duplicate_file_iter))

                self.write([''.join(seq_to_write), filename], output_dir)
                probes_in_current_file = 0
                seq_to_write = list()
                file_number += 1
            i += 1

    @staticmethod
    def write(data, output_dir):
        """
        This method creates the gene fasta file
        :param data: A data representation of a .fasta file
        :param output_dir: The path of the output dir
        """

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filename = output_dir + data[1]
        # Open the file.

        if os.path.exists(filename):
            duplicate_file_iter = 1

            while os.path.exists(filename+'({0})'.format(str(duplicate_file_iter))):
                duplicate_file_iter += 1

            print('[WARNING] File: ',
                  filename,
                  ' Exists.\n\t Created: ',
                  filename, '({0}) instead'.format(str(duplicate_file_iter)))
            filename += '({0})'.format(str(duplicate_file_iter))

            file = open(filename, 'w')
            if type(data) == list:
                file.write(''.join(data[0]))
            elif type(data) == str:
                file.write(data[0])
            file.close()

        else:
            file = open(filename, 'w')

            if type(data) == list:
                file.write(''.join(data[0]))
            elif type(data) == str:
                file.write(data[0])
            file.close()

        return filename