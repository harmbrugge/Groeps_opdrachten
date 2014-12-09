#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os


class Prober:
    def __init__(self):
        self.probes = list()
        self.trans_table = str.maketrans("atcg", "tagc")

    def make_probes(self, genes):

        # repeat_single_nuc = re.compile(r'(.)\1{3}')
        # repeat_di_nuc = re.compile(r'(.{2})\1{2}')

        for gene in genes:
            for i in range(0, len(gene.exon_seqs)-20):
                cur_probe_id = i
                cur_probe = gene.exon_seqs[i:i+20]

                if not re.search(r'(.)\1{3}', cur_probe):
                    if not re.search(r'(.{2})\1{2}', cur_probe):
                        # Pak alleen het gebied na 5 + 3(gap)
                        hairpin_domain = cur_probe[8:]
                        hairpin_bool = False

                        # Pak alle mogelijke sequenties van 5 in hairpin_domain
                        for y in range(0, len(hairpin_domain)-5):
                            hairpin_seq = hairpin_domain[y:y+5]
                            # Maak de sequenties reverse complement
                            hairpin_seq_rev_com = hairpin_seq.translate(self.trans_table)[::-1]

                            # Zoek op de probe naar de sequentie rekening houdens met eindlocatie
                            if hairpin_seq_rev_com in cur_probe[:y+5]:
                                hairpin_bool = True
                                break

                        if not hairpin_bool:
                            self.probes.append(Probes(cur_probe_id, gene.gene_id, gene.chromosome_id, cur_probe))

        print(len(self.probes))


class Probes:

    def __init__(self, probe_id, gene_id, chromosome_id, sequence):
        self.probe_id = probe_id
        self.gene_id = gene_id
        self.chromosome_id = chromosome_id
        self.sequence = sequence


def main():

    for file in glob.glob(os.path.join('/Users/harmbrugge/Documents/Bio-inf/Thema06/plasmodium', '*.gbk')):
        genbank = genbank_parser.GenBank(filename=file)
        genbank.make_chromosome()
        genes = genbank.make_genes()
        Prober().make_probes(genes)

if __name__ == '__main__':
    main()

