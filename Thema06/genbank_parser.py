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
        pass

    def make_genes(self):
        pass

print(GenBank('chromosome_1.gb'))