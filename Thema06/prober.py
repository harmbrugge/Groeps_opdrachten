#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os


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
        #gene = genes[0]
        for gene in genes:
            for i in range(0, len(gene.exon_seqs)-20):
                cur_probe_id = i
                cur_probe = gene.exon_seqs[i:i+20]

                if not re.search(repeat_single_nuc, cur_probe):
                    if not re.search(repeat_di_nuc, cur_probe):
                        # Pak alleen het gebied van 5 + 3(gap)
                        hairpin_domain = cur_probe[8:]
                        hairpin_bool = False
                        # Pak alle mogelijke sequenties van 5 in hairpin_domain
                        for y in range(0, len(hairpin_domain)-5):

                            if hairpin_bool:
                                break

                            hairpin_seq = hairpin_domain[y:y+5]
                            # Maak de sequenties reverse complement
                            hairpin_seq_rev = hairpin_seq[::-1]
                            hairpin_seq_rev_com = hairpin_seq_rev.translate(trans_table)

                            # Zoek op de probe naar de sequentie rekening houdens met eindlocatie
                            hairpin_seq_pos = cur_probe.find(hairpin_seq_rev_com, 0, 5+y)
                            if hairpin_seq_pos != -1:
                                hairpin_bool = True

                        if hairpin_bool is False:
                            self.probes.append(Probes(cur_probe_id, gene.gene_id, gene.chromosome_id, cur_probe))

        print(len(self.probes))


class Probes:

    def __init__(self, probe_id, gene_id, chromosome_id, sequence):
        self.probe_id = probe_id
        self.gene_id = gene_id
        self.chromosome_id = chromosome_id
        self.sequence = sequence


def main():

    for file in glob.glob(os.path.join('E:\Dropbox\Thema6\plasmodium', '*.gbk')):
        genbank = genbank_parser.GenBank(filename=file)
        genbank.make_chromosome()
        genes = genbank.make_genes()
        Prober().make_probes(genes)


if __name__ == '__main__':
    main()

