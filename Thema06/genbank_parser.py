#!/usr/bin/env python3
import re


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
                exon_regions[i] =  exon.split('..')

            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)
            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)
            print(protein_name)
            #
            # print(strand)
            # print(exon_regions)



class Chromosome:

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism


class Gene:
    def __init__(self, gene_id, chromosome_id, strand, exons, protein, protein_id):
        self.gene_id = gene_id
        self.chromosome_id = chromosome_id
        self.strand = strand
        self.exons = exons
        self.protein = protein
        self.protein_id = protein_id

genBank = GenBank('chromosome_1.gb')

chromosome1 = genBank.make_chromosome()
genBank.make_genes()
# print(chromosome1.chromosome_id)
# print(chromosome1.organism)
# print(chromosome1.seq)
