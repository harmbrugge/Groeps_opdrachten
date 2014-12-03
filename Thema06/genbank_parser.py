#!/usr/bin/env python3
import re
import os


# TODO error/exception handeling!!
class GenBank:
    """
    This class handles the interactions pretaining to the genbank file.
    It's also responsible for creating the chromosome and gene objects.
    The data from the genbank file is stored in 1 large string, so this
    script is non streaming. We opted for this option because we thought
    the code would more flexible this way.
    """

    def __init__(self, file):
        """
        file_string:        The string containing the entire genbank file.
        chromosome:         The chromosome object for the genbank file.
        genes:              A list of gene objects for the chromosome
        :param file:        The path + filename for the genbank file one wishes to excecute.
        """
        self.file_string = str()

        if type(file) == str:
            self.file_string = file
        else:
            self.file = file
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

        try:
            # The regex code that searches for the mt chromosome.
            definition = re.search('DEFINITION\s*(.*)\s(mitochondrion)', self.file_string)
            if definition:
                definition = definition
            else:
                # If no mitochondrion is present.
                definition = re.search('DEFINITION\s*(.*)\schromosome\s(\d*|\w*)', self.file_string)

            organism = definition.group(1).replace(",", "")
            chromosome_id = definition.group(2)

            seq = re.search('ORIGIN(.*)//', self.file_string, re.DOTALL).group(1)
            seq = re.sub('\n|\s|\d', '', seq).lower()

            self.chromosome = Chromosome(seq, chromosome_id, organism)

        except AttributeError:
            print('the styling of the file was not correct.')

        return self.chromosome

    def make_genes(self):
        """
        This method handles the creation of the gene objects.
        :return: A list of gene objects.
        """

        # The regex to get all of the coding DNA seqeunces.
        cds_info = re.findall('CDS(.+?)/translation', self.file_string, re.DOTALL)
        # Creates the dict for the creation of an reverse complement.
        trans_table = str.maketrans("atcg", "tagc")
        gene_list = list()
        strand = str()

        for cur_cds in cds_info:

            # The regex to get all of the info from an cds.
            exon_seqs = list()
            exon_regions = re.findall('.(\d*)\.\.>?(\d*)', cur_cds, re.DOTALL)
            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)
            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
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

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism
        self.genes = None


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


class FastaWriter:
    """
    The class that handles the creation of the fasta files.
    """

    @staticmethod
    def get_gene_string(genes):
        """
        This method creates the gene fasta file
        :param genes: A list of Gene objects
        :param output_dir: The path of the output dir
        """

        # The creation of the filename .
        gene_list = list()
        filename = 'chromosome-' \
                   + genes[0].chromosome_id \
                   + '_' + genes[0].organism.replace(' ', '-')\
                   + '_genes'

        for gene in genes:

            # Creation of the fasta id.
            gen_seq = gene.exon_seqs
            seq_to_write = list()

            seq_to_write.append('>gene_'
                                + str(gene.gene_id)
                                + '|' + str(gene.strand)
                                + '|' + str(gene.protein) + '\n')

            for i in range(0, len(gen_seq), 75):
                seq_to_write.append(gen_seq[i:i+75] + '\n')

            gene_list.append(''.join(seq_to_write) + '\n\n')

        return [''.join(gene_list), filename]

    @staticmethod
    def get_chromosome_string(chromosome):

        filename = 'chromosome_' \
                   + str(chromosome.chromosome_id) \
                   + '_' + str(chromosome.organism.replace(' ', '-'))

        # Creation of the fasta id.
        fasta_id = '>chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism) + '\n'

        # Add a newline char every 75 chars
        seq_to_write = []
        for i in range(0, len(chromosome.seq), 75):
            seq_to_write.append(chromosome.seq[i:i+75])

        file_string = fasta_id + '\n'.join(seq_to_write)

        return [file_string, filename]

    @staticmethod
    def write_genes(gene_string, output_dir):
        """
        This method creates the gene fasta file
        :param genes: A list of Gene objects
        :param output_dir: The path of the output dir
        """
        # The creation of the filename .
        filename = output_dir + 'chromosome-' \
                              + genes[0].chromosome_id \
                              + '_' + genes[0].organism.replace(' ', '-')\
                              + '_genes' \
                              + '.fa'

        if os.path.exists(filename):
            print('Fasta file', filename, 'exists already')

        else:
            # Open the file.
            file = open(filename, 'w')
            file.write(gene_string)
            file.close()

        return filename

    @staticmethod
    def write_chromosome(chromosome_string, output_dir):

        # The creation of the filename .
        filename = output_dir \
                + 'chromosome_' \
                + str(chromosome_string.chromosome_id) \
                + '_' + str(chromosome_string.organism.replace(' ', '-')) + '.fa'

        # Check if the file exists
        if os.path.exists(filename):
            print('Chromosome', filename, 'file exists already')

        else:

            file = open(filename, 'w')
            file.write(chromosome_string)
            file.close()

        return filename
