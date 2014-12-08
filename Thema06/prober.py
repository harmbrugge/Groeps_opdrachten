import genbank_parser
import re


class Prober:
    def __init__(self):
        self.probes = list()
        self.niks = None

    def make_probes(self, genes):
        trans_table = str.maketrans("atcg", "tagc")

        for gene in genes:
            gene.exon_seqs = gene.exon_seqs.translate(trans_table)[::-1]
            for i in range(0, len(gene.exon_seqs)-20):
                cur_probe = gene.exon_seqs[i:i+20]
                # print(cur_probe)
                if not re.match('(.)\\1{3}', cur_probe):
                    if not re.match('(.{2})\\1{3}', cur_probe):

                        print(cur_probe)


def main():
    genbank = genbank_parser.GenBank(filename="NC_004325.gbk")
    genbank.make_chromosome()
    genes = genbank.make_genes()
    Prober().make_probes(genes)


if __name__ == '__main__':
    main()

