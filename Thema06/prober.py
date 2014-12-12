#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os


class Prober:

    def __init__(self):
        self.possible_probe_count = 0
        self.probe_count = 0
        self.trans_table = str.maketrans("atcg", "tagc")
        self.mono_count = 0
        self.di_count = 0
        self.hairpin_count = 0

    def make_probes(self, gene, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):

        i = 0

        probes = list()

        while i < len(gene.exon_seqs) - probe_length:
            self.possible_probe_count += 1
            cur_probe = gene.exon_seqs[i:i+probe_length]

            # Zoek naar 4-nuc-mono-repeats
            nuc_mono_repeat = '(\w)\\1{' + str(nr_nuc_mono_repeat) + '}'
            nuc_di_repeat = '(\w{2,3})\\1{' + str(nr_nuc_di_repeat) + '}'

            if not re.search(nuc_mono_repeat, cur_probe):
                # Zoek naar 3-nuc-di-repeats
                if not re.search(nuc_di_repeat, cur_probe):

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
                            self.hairpin_count += 1
                            hairpin_bool = True
                            break

                    if not hairpin_bool:
                        # tel 10 locatie op als geschikte probe is gevonden en construct probe object
                        i += coverage
                        self.probe_count += 1
                        fraction = (i+1) / len(gene.exon_seqs)

                        probes.append(Probes(i, cur_probe, fraction))
                else:
                    self.di_count += 1
            else:
                self.mono_count += 1

            i += 1
        return probes


class Probes:

    def __init__(self, probe_id, sequence, fraction):
        self.probe_id = probe_id
        self.sequence = sequence
        self.fraction = fraction


def main():

    gene_list = list()
    prober = Prober()

    for file in glob.glob(os.path.join('genbank_files/', '*.gbk')):

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()

        cur_gene_list = genbank_parser.FastaWriter.get_gene_string(chromosome.genes)
        gene_list.append(cur_gene_list)

        for gene in chromosome.genes:
            gene.probes = prober.make_probes(gene)

        print('CHROMOSOME ID:', chromosome.chromosome_id, ' GENE COUNT:', len(chromosome.genes))
        probe_list = genbank_parser.FastaWriter.get_probe_string(chromosome.genes)
        genbank_parser.FastaWriter.write(probe_list)

    print('Possible probes:', prober.possible_probe_count)
    print('Mono repeat count:', prober.mono_count, 100 * prober.mono_count / prober.possible_probe_count)
    print('Di repeat count:', prober.di_count, 100 * prober.di_count / prober.possible_probe_count)
    print('Hairpin count:', prober.hairpin_count, 100 * prober.hairpin_count / prober.possible_probe_count)
    print('Probe count:', prober.probe_count, 100 * prober.probe_count / prober.possible_probe_count)

    genbank_parser.FastaWriter.write_list(gene_list)

if __name__ == '__main__':
    main()