#!/usr/bin/env python3
import genbank_parser
import re


class Prober:
    def __init__(self):
        self.probes = list()
        self.niks = None

    def make_probes(self, genes):
        trans_table = str.maketrans("atcg", "tagc")

        for gene in genes:
            #gene.exon_seqs = gene.exon_seqs.translate(trans_table)[::-1]

            for i in range(0, len(gene.exon_seqs)-20):
                cur_probe = gene.exon_seqs[i:i+20]
                # print(cur_probe)

                if not re.match('(.)\\1{3}', cur_probe):

                    if not re.match('(.{2})\\1{3}', cur_probe):
                        rev_cur_probe = cur_probe.translate(trans_table)[::-1]
                        #comp_list = [rev_cur_probe[y:y+5] for y in range(0, int(len(rev_cur_probe)/2))]

                        for y in range(0, int(len(rev_cur_probe)/2)):
                            comp = rev_cur_probe[y:y+5]
                            hairpin_seq_pos = cur_probe.find(comp, y+8, len(cur_probe))
                            if hairpin_seq_pos != -1:
                                print(comp)
                                print(comp.translate(trans_table)[::-1])
                                print(cur_probe)
                            # hairpin_comp_seq = cur_probe.find(comp.translate(trans_table)[::-1], 0, len(cur_probe))
                            # if hairpin_seq_pos + 8 < hairpin_comp_seq and hairpin_seq_pos != -1 and hairpin_comp_seq != -1:





def main():
    genbank = genbank_parser.GenBank(filename="NC_004325.gbk")
    genbank.make_chromosome()
    genes = genbank.make_genes()
    Prober().make_probes(genes)


if __name__ == '__main__':
    main()

