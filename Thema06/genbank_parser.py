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
        pass


class Chromosome:

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism


class Gene:
    def __init__(self, gene_id, chromosome_id, exons, protein, protein_id):

        pass

genBank = GenBank('chromosome_1.gb')

chromosome1 = genBank.make_chromosome()
print(chromosome1.chromosome_id)
print(chromosome1.organism)
print(chromosome1.seq)
