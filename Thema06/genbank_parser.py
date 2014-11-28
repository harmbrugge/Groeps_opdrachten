#!/usr/bin/env python3
import re
import os


class GenBank:

    def __init__(self, file):
        self.seq = str()
        self.file = file
        self._read_file()

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

        return Chromosome(seq, chromosome_id, organism)

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

            # TODO figure out a way to get the chromosome id

            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)
            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)

            gene_list.append(Gene(gene_id, strand, exon_regions, protein_name, protein_id))

        return gene_list


class Chromosome:

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism

    def make_fasta(self):
        filename = 'chromosome' + str(self.chromosome_id) + '_' + str(self.organism)

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection!

        else:
            file = open(filename,'w')
            fasta_id = '>chromosome_' + str(self.chromosome_id) + '|' + str(self.organism) + '\n'
            file.write(fasta_id)

            seq_to_write= []
            for i in range(0, len(self.seq), 75):
                seq_to_write.append(self.seq[i:i+75])

            file.write('\n'.join(seq_to_write))
            file.close()


class Gene:

    def __init__(self, gene_id, strand, exons, protein, protein_id, chromosome_id=1):
        self.gene_id = gene_id
        self.chromosome_id = chromosome_id
        self.strand = strand
        self.exons = exons
        self.protein = protein
        self.protein_id = protein_id


def make_fasta_genes():
    # TODO fix this so it works properly maybe move the method to the genbank object
    filename = 'chromosome' + str(1) + '_' + str('Plasmodium falciparum strain 3D7') + '_genes'

    if os.path.exists(filename):
        print('file exists already')
        # TODO build proper naming and path selection!

    else:
        file = open(filename, 'w')
        # TODO make it so that the seqeunce is written to the file
        for obj in GenBank('chromosome_1.gb').make_genes():
            fasta_id = '>gene_' + str(obj.gene_id) + '|' + str(obj.strand) + '|' + str(obj.protein) + '\n'
            file.write(fasta_id)

            # seq_to_write = []
            # for i in range(0, len(obj.seq), 75):
            #     seq_to_write.append(obj.seq[i:i+75])
            # file.write('\n'.join(seq_to_write))

        file.close()


def main():
    genbank = GenBank('chromosome_1.gb')
    chromosome1 = genbank.make_chromosome()
    chromosome1.make_fasta()
    make_fasta_genes()

if __name__ == '__main__':
    main()










# for gene_obj in genBank.make_genes():
#     print('------------------------------------')
#     print(gene_obj.gene_id)
#     print(gene_obj.strand)
#     print(gene_obj.exons)
#     print(gene_obj.protein)
#     print(gene_obj.protein_id)
#     print('------------------------------------')
# # print(chromosome1.chromosome_id)
# print(chromosome1.organism)
# print(chromosome1.seq)
