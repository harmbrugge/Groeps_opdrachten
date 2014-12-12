#!/usr/bin/env python3
import genbank_parser
import glob
import os


class ParserHandler:

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.genbank = None
        self.chromosome = None
        self.genes = None
        self.fasta_witer = None

    def open_file(self):

        for filename in glob.glob(os.path.join(self.input_folder, '*.gbk')):
            self.genbank = genbank_parser.GenBank(filename)
            self.fasta_witer = genbank_parser.FastaWriter()
            self.create_chromosome_fasta()
            self.create_genes_fasta()

    def create_chromosome_fasta(self):

        self.chromosome = self.fasta_witer.get_chromosome_string(self.genbank.make_chromosome())
        self.fasta_witer.write_chromosome(self.chromosome, self.output_folder)

    def create_genes_fasta(self):

        self.genes = self.fasta_witer.get_gene_string(self.genbank.make_genes())
        self.fasta_witer.write_genes(self.genes, self.output_folder)


def main():
    p = ParserHandler('E:\Dropbox\Thema6', 'plasmodium/')
    p.open_file()
    p.create_chromosome_fasta()



if __name__ == '__main__':
    main()
