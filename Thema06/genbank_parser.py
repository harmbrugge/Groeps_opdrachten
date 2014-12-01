#!/usr/bin/env python3
import re
import os


# TODO error/exception handeling!!
class GenBank:

    def __init__(self, file):

        self.file_string = str()
        self.file = file
        self._read_file()
        self.chromosome = None
        self.genes = None

    def __str__(self):
        return self.file_string

    def _read_file(self):

        handle = open(self.file, 'r')
        var = handle.readlines()
        self.file_string = ''.join(var)
        handle.close()     

    def make_chromosome(self):

        try:
            # So the mt chromosome is picked up.
            definition = re.search('DEFINITION\s*(.*)\s(mitochondrion)', self.file_string)
            if definition:
                definition = definition
            else:
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

        cds_info = re.findall('CDS(.+?)/translation', self.file_string, re.DOTALL)
        trans_table = str.maketrans("atcg", "tagc")
        gene_list = list()
        strand = str()

        for cur_cds in cds_info:

            exon_seqs = list()
            exon_regions = re.findall('.(\d*)\.\.>?(\d*)', cur_cds, re.DOTALL)
            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)
            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)

            for i, exon in enumerate(exon_regions):

                if re.match('.*complement', cur_cds):
                    strand = '-'
                    gen_seq = self.chromosome.seq[int(exon[0]):int(exon[1])][::-1]
                    gen_seq = gen_seq.translate(trans_table)
                    exon_seqs.append(gen_seq)

                else:
                    strand = '+'
                    gen_seq = self.chromosome.seq[int(exon[0])-1:int(exon[1])-1]
                    exon_seqs.append(gen_seq)

            if strand == '-':
                exon_seqs = ''.join(exon_seqs[::-1])

            elif strand == '+':
                exon_seqs = ''.join(exon_seqs)

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

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism
        self.genes = None


class Gene:

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

    # TODO create innit containing the path to output dir.
    @staticmethod
    def write_genes(genes, output_dir):
        filename = output_dir + 'chromosome-' + genes[0].chromosome_id + '_' + genes[0].organism.replace(' ', '-') + '_genes'

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection! (kinda done)

        else:
            file = open(filename, 'w')
            for gene in genes:

                fasta_id = '>gene_' + str(gene.gene_id) + '|' + str(gene.strand) + '|' + str(gene.protein) + '\n'
                file.write(fasta_id)
                gen_seq = gene.exon_seqs
                seq_to_write = list()

                for i in range(0, len(gen_seq), 75):
                    seq_to_write.append(gen_seq[i:i+75])
                file.write('\n'.join(seq_to_write) + '\n\n')

            file.close()

    @staticmethod
    def write_chromosome(chromosome, output_dir):
        filename = output_dir + 'chromosome_' + str(chromosome.chromosome_id) + '_' + str(chromosome.organism.replace(' ', '-'))

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection! (kinda done)

        else:
            file = open(filename, 'w')
            fasta_id = '>chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism) + '\n'
            file.write(fasta_id)

            seq_to_write = []
            for i in range(0, len(chromosome.seq), 75):
                seq_to_write.append(chromosome.seq[i:i+75])

            file.write('\n'.join(seq_to_write))
            file.close()
