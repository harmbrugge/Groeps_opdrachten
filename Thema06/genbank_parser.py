#!/usr/bin/env python3
import re

class GenBank:

    def __init__(self, file):
        self.seq = None
        self.file = file
        self._read_file()

    def _read_file(self):
        handle = open(self.file, 'r')
        for line in handle:
            self.seq += line
        handle.close()     

    def make_chromosome(self):
        pass

    def make_genes(self):
        pass