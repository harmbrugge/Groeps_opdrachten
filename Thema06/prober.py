#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os


class Prober:
    def __init__(self):
        self.probe_count = 0
        self.trans_table = str.maketrans("atcg", "tagc")

    def make_probes(self, gene):

        i = 0
        probes = list()
        while i < len(gene.exon_seqs)-20:
            cur_probe = gene.exon_seqs[i:i+20]

            # Zoek naar 4-nuc-mono-repeats
            if not re.search(r'(\w)\1{3}', cur_probe):
                # Zoek naar 3-nuc-di-repeats
                if not re.search(r'(\w{2})\1{2}', cur_probe):

                    # Pak alleen het gebied na 5(hairpin sequentie) + 3(gap)
                    hairpin_domain = cur_probe[8:]
                    hairpin_bool = False

                    # Pak alle mogelijke sequenties van 5 in hairpin_domain
                    for y in range(0, len(hairpin_domain)-5):
                        hairpin_seq = hairpin_domain[y:y+5]
                        # Maak de sequenties reverse complement
                        hairpin_seq_rev_com = hairpin_seq.translate(self.trans_table)[::-1]

                        # Zoek op de probe naar de sequentie rekening houdend met eindlocatie
                        if hairpin_seq_rev_com in cur_probe[:y+5]:
                            hairpin_bool = True
                            break

                    if not hairpin_bool:
                        # tel 10 locatie op als geschikte probe is gevonden en construct probe object
                        i += 10
                        self.probe_count += 1
                        probes.append(Probes(i, cur_probe))
            i += 1

        return probes


class Probes:

    def __init__(self, probe_id, sequence):
        self.probe_id = probe_id
        self.sequence = sequence


def main():

    prober = Prober()
    for file in glob.glob(os.path.join('genbank_files/', '*.gbk')):

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()

        for gene in chromosome.genes:
            gene.probes = prober.make_probes(gene)

        probe_list = genbank_parser.FastaWriter.get_probe_string(chromosome.genes)
        genbank_parser.FastaWriter.write(probe_list)

    print(prober.probe_count)

if __name__ == '__main__':
    main()

