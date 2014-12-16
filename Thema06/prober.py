#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os
import database_functions
import time


class Prober:

    def __init__(self, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):

        self.nr_nuc_mono_repeat = nr_nuc_mono_repeat
        self.nr_nuc_di_repeat = nr_nuc_di_repeat
        self.probe_length = probe_length
        self.coverage = coverage

        self.trans_table = str.maketrans("atcg", "tagc")
        self.possible_probe_count = 0
        self.probe_count = 0
        self.mono_count = 0
        self.di_count = 0
        self.hairpin_count = 0

        self.id = None

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
        self.cg_perc = None
        self.temp_melt = None


def main():
    start_time = time.time()

    nr_nuc_mono_repeat = 3
    nr_nuc_di_repeat = 2
    probe_length = 20
    coverage = 10

    prober = Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                    nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                    probe_length=probe_length,
                    coverage=coverage)

    chromosome_list = list()

    # loop over gbk files genbank dir
    for file in glob.glob(os.path.join('genbank_files/', '*.gbk')):
        # read genbank file
        genbank = genbank_parser.GenBank(filename=file)

        # make chromsome, gene & probe objects
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()
        for gene in chromosome.genes:
            gene.probes = prober.make_probes(gene)

        chromosome_list.append(chromosome)
        print('Done with chromsome:', chromosome.chromosome_id)

    # open a DB connection
    database = database_functions.Database()
    database.open_connection()

    # set data to DB
    database.set_probe_experiment(prober)
    for chromosome in chromosome_list:
        database.set_chromosome(chromosome)
        print('Chromsome set to DB:', chromosome.chromosome_id)

        for gene in chromosome.genes:
            database.set_gene(gene, chromosome.chromosome_id)
            database.set_probes(prober, gene)
        print('Genes set to DB:', chromosome.chromosome_id)
        print('Probes set to DB:', chromosome.chromosome_id)

    database.close_connection()

    print(time.time()-start_time)

if __name__ == '__main__':
    main()