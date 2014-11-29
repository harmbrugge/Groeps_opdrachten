#!/usr/bin/env python3
import re
import os


class GenBank:

    def __init__(self, file):
        self.seq = str()
        self.file = file
        self._read_file()
        self.chromosome = None
        self.genes = None

    def __str__(self):
        return self.seq

    def _read_file(self):
        handle = open(self.file, 'r')
        var = handle.readlines()
        self.seq = ''.join(var)
        handle.close()     

    def make_chromosome(self):
        definition = re.search('DEFINITION\s*(.*),\schromosome\s(\d|\w{1,2})', self.seq)
        organism = definition.group(1)
        chromosome_id = definition.group(2)

        seq = re.search('ORIGIN(.*)//', self.seq, re.DOTALL).group(1)
        seq = re.sub('\n|\s|\d', '', seq)

        self.chromosome = Chromosome(seq, chromosome_id, organism)

        return self.chromosome

    def make_genes(self):

        cds_info = re.findall('CDS(.+?)/translation', self.seq, re.DOTALL)
        gene_list = []

        for cur_cds in cds_info:

            if re.match('.*complement', cur_cds):
                strand = '+'
            else:
                strand = '-'
            exon_regions = re.findall('.(\d*\.\.\d*)', cur_cds, re.DOTALL)

            for i, exon in enumerate(exon_regions):
                exon_regions[i] = exon.split('..')

            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)
            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)

            gene_list.append(Gene(gene_id, strand, exon_regions, protein_name, protein_id,
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

    def __init__(self, gene_id, strand, exons, protein, protein_id, chromosome):
        self.gene_id = gene_id
        self.chromosome_id = chromosome.chromosome_id
        self.organism = chromosome.organism
        self.strand = strand
        self.exons = exons
        self.protein = protein
        self.protein_id = protein_id


class FastaHandler:

    def __init__(self):
        pass

    def write_genes(self, genes):
        filename = 'chromosome' + genes[0].chromosome_id + '_' + genes[0].organism + '_genes'

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection!

        else:
            file = open(filename, 'w')
            # TODO make it so that the seqeunce is written to the file
            for gene in genes:
                fasta_id = '>gene_' + str(gene.gene_id) + '|' + str(gene.strand) + '|' + str(gene.protein) + '\n'
                file.write(fasta_id)

                # seq_to_write = []
                # for i in range(0, len(gene.seq), 75):
                #     seq_to_write.append(gene.seq[i:i+75])
                # file.write('\n'.join(seq_to_write))

            file.close()

    def write_chromosome(self, chromosome):
        filename = 'chromosome' + str(chromosome.chromosome_id) + '_' + str(chromosome.organism)

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection!

        else:
            file = open(filename, 'w')
            fasta_id = '>chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism) + '\n'
            file.write(fasta_id)

            seq_to_write = []
            for i in range(0, len(chromosome.seq), 75):
                seq_to_write.append(chromosome.seq[i:i+75])

            file.write('\n'.join(seq_to_write))
            file.close()


def main():
    genbank = GenBank('chromosome_1.gb')
    chromosome1 = genbank.make_chromosome()
    chromosome1.genes = genbank.make_genes()

    fasta_handler = FastaHandler()
    fasta_handler.write_chromosome(chromosome1)
    fasta_handler.write_genes(chromosome1.genes)


if __name__ == '__main__':
    main()
