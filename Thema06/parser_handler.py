import genbank_parser


class





def main():

    # /homes/obbakker/Dropbox/Thema6/plasmodium/NC_000910.gbk
    genbank = genbank_parser.GenBank('/homes/obbakker/Dropbox/Thema6/plasmodium/NC_000910.gbk')
    chromosome1 = genbank.make_chromosome()
    chromosome1.genes = genbank.make_genes()

    fasta_handler = genbank_parser.FastaHandler()
    fasta_handler.write_chromosome(chromosome1)
    fasta_handler.write_genes(chromosome1.genes)


if __name__ == '__main__':
    main()
