#!/usr/bin/env python3
import genbank_parser
import re


class Prober:
    def __init__(self):
        self.probes = list()
        self.niks = None

    def make_probes(self, genes):
        trans_table = str.maketrans("atcg", "tagc")

        repeat_single_nuc = re.compile(r'(.)\1{3}')
        repeat_di_nuc = re.compile(r'(.{2})\1{2}')

        #for gene in genes:
            #gene.exon_seqs = gene.exon_seqs.translate(trans_table)[::-1]
        gene = genes[0]

        for i in range(0, len(gene.exon_seqs)-20):
            cur_probe_id = i
            cur_probe = gene.exon_seqs[i:i+20]

            if not re.search(repeat_single_nuc, cur_probe):
                if not re.search(repeat_di_nuc, cur_probe):
                    # Pak alleen het gebied van 5 + 3(gap)
                    hairpin_domain = cur_probe[8:]

                    # Pak alle mogelijke sequenties van 5 in hairpin_domain
                    for y in range(0, len(hairpin_domain)-5):
                        hairpin_seq = hairpin_domain[y:y+5]

                        # Maak de sequenties reverse complement
                        hairpin_seq_rev = hairpin_seq[::-1]
                        hairpin_seq_rev_com = hairpin_seq_rev.translate(trans_table)

                        # Zoek op de probe naar de sequentie rekening houdens met eindlocatie
                        hairpin_seq_pos = cur_probe.find(hairpin_seq_rev_com, 0, 5+y)
                        if hairpin_seq_pos != -1:
                            print(cur_probe_id)
                            print(cur_probe)
                            print(hairpin_seq_rev_com)
                            print()
                            print('--------------')


def main():
    genbank = genbank_parser.GenBank(filename="NC_004325.gbk")
    genbank.make_chromosome()
    genes = genbank.make_genes()
    Prober().make_probes(genes)


if __name__ == '__main__':
    main()

