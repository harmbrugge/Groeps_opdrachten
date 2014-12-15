#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os
import datetime
import database_functions
import sys
import time


class Prober:

    def __init__(self, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):

        self.nr_nuc_mono_repeat = nr_nuc_mono_repeat
        self.nr_nuc_di_repeat = nr_nuc_di_repeat
        self.probe_length = probe_length
        self.coverage = coverage

        self.probes = None

        self.trans_table = str.maketrans("atcg", "tagc")
        self.possible_probe_count = 0
        self.probe_count = 0
        self.mono_count = 0
        self.di_count = 0
        self.hairpin_count = 0

    def make_probes(self, gene):

        i = 0
        mono_time_list = []
        di_time_list = []
        hairpin_time_list = []
        probes = list()

        while i < len(gene.exon_seqs) - self.probe_length:

            gene.possible_probe_count += 1
            self.possible_probe_count += 1

            cur_probe = gene.exon_seqs[i:i+self.probe_length]
            start_time = time.time()

            # Zoek naar 4-nuc-mono-repeats
            nuc_mono_repeat = '(\w)\\1{' + str(self.nr_nuc_mono_repeat) + '}'
            nuc_di_repeat = '(\w{2,3})\\1{' + str(self.nr_nuc_di_repeat) + '}'

            if not re.search(nuc_mono_repeat, cur_probe):
                mono_time_list.append(time.time()-start_time)
                # Zoek naar 3-nuc-di-repeats
                start_time = time.time()
                if not re.search(nuc_di_repeat, cur_probe):

                    # Pak alleen het gebied na 5(hairpin sequentie) + 3(gap)
                    hairpin_domain = cur_probe[8:]
                    hairpin_bool = False
                    di_time_list.append(time.time()-start_time)
                    # Pak alle mogelijke sequenties van 5 in hairpin_domain
                    start_time = time.time()
                    for y in range(0, len(hairpin_domain)-5):
                        hairpin_seq = hairpin_domain[y:y+5]

                        # Maak de sequenties reverse complement
                        hairpin_seq_rev_com = hairpin_seq.translate(self.trans_table)[::-1]

                        # Zoek op de probe naar de sequentie rekening houdend met eindlocatie
                        if hairpin_seq_rev_com in cur_probe[:y+5]:
                            gene.hairpin_count += 1
                            self.hairpin_count += 1
                            hairpin_bool = True
                            break

                    hairpin_time_list.append(time.time()-start_time)

                    if not hairpin_bool:
                        # tel 10 locatie op als geschikte probe is gevonden en construct probe object
                        i += self.coverage
                        gene.probe_count += 1
                        self.probe_count += 1
                        fraction = (i+1) / len(gene.exon_seqs)

                        probes.append(Probes(i, cur_probe, fraction))

                else:
                    self.di_count += 1
                    gene.di_count += 1
                    mono_time_list.append(time.time()-start_time)
            else:
                self.mono_count += 1
                gene.mono_count += 1
                mono_time_list.append(time.time()-start_time)

            i += 1

        return probes


class Probes:

    def __init__(self, probe_id, sequence, fraction):
        self.probe_id = probe_id
        self.sequence = sequence
        self.fraction = fraction


class Handler:

    @staticmethod
    def handler(chromosome, gb_obj_size, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):
        # TODO finalize the database model and implement it so the code can be eddit tow rok with this.

        start_time = time.time()
        prober = Prober()

        for gene in chromosome.genes:
            gene.probes = prober.make_probes(gene)

        # Close the cursor object.
        database.close_cursor()


def main():
    chromosome_list = []

    database = database_functions.Dynamic()
    database.get_cursor()

    for file in glob.glob(os.path.join('genbank_files/', '*.gbk')):
        # Construct gene and chromosome objects.
        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()

        chromosome.genes = genbank.make_genes()
        chromosome_list.append(chromosome)

        Handler().handler(chromosome=chromosome,
                          gb_obj_size=sys.getsizeof(genbank.file_string))

if __name__ == '__main__':
    main()
    #C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit timeit C:\python34\python prober.py