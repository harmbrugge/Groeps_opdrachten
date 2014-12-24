#!/usr/bin/env python3
import re
import time


class Prober:

    def __init__(self, nr_nuc_mono_repeat=3,
                 nr_nuc_di_repeat=2,
                 probe_length=20,
                 nucleotide_frame_skip=2,
                 min_gc_percentage=50):

        self.nr_nuc_mono_repeat = nr_nuc_mono_repeat
        self.nr_nuc_di_repeat = nr_nuc_di_repeat
        self.probe_length = probe_length
        self.nucleotide_frame_skip = nucleotide_frame_skip
        self.min_gc_percentage = min_gc_percentage
        self.id = None

        self.trans_table = str.maketrans("atcg", "tagc")

    def make_probes(self, gene, skip_bool):

        i = 0
        start_time_total = time.clock()
        mono_time_list = []
        di_time_list = []
        hairpin_time_list = []
        gc_time_list = []

        possible_probe_count = 0
        probe_count = 0
        mono_count = 0
        di_count = 0
        hairpin_count = 0
        gc_count = 0

        probes = list()

        while i < len(gene.exon_seqs) - self.probe_length:

            possible_probe_count += 1
            cur_probe = gene.exon_seqs[i:i+self.probe_length]
            start_time = time.clock()

            cur_c_count = cur_probe.count('c')
            cur_g_count = cur_probe.count('g')
            cur_a_count = cur_probe.count('a')
            cur_t_count = cur_probe.count('t')

            if cur_g_count == 0 and cur_c_count == 0:
                cur_gc_perc = 0
            else:
                cur_gc_perc = (cur_c_count + cur_g_count) / self.probe_length * 100

            if cur_gc_perc > self.min_gc_percentage:
                gc_time_list.append(time.clock() - start_time)
                start_time = time.clock()

                # Zoek naar 4-nuc-mono-repeats
                nuc_mono_repeat = '(\w)\\1{' + str(self.nr_nuc_mono_repeat) + '}'
                nuc_di_repeat = '(\w{2,3})\\1{' + str(self.nr_nuc_di_repeat) + '}'

                mono_search = re.search(nuc_mono_repeat, cur_probe)
                if not mono_search:

                    mono_time_list.append(time.clock()-start_time)
                    # Zoek naar 3-nuc-di-repeats
                    start_time = time.clock()

                    di_search = re.search(nuc_di_repeat, cur_probe)
                    if not di_search:
                        di_time_list.append(time.clock()-start_time)
                        # Pak alleen het gebied na 5(hairpin sequentie) + 3(gap)

                        start_time = time.clock()
                        hairpin_domain = cur_probe[8:]
                        hairpin_bool = False

                        # Pak alle mogelijke sequenties van 5 in hairpin_domain

                        for y in range(0, len(hairpin_domain)-5):
                            hairpin_seq = hairpin_domain[y:y+5]

                            # Maak de sequenties reverse complement
                            hairpin_seq_rev_com = hairpin_seq.translate(self.trans_table)[::-1]

                            # Zoek op de probe naar de sequentie rekening houdend met eindlocatie
                            if hairpin_seq_rev_com in cur_probe[:y+5]:
                                hairpin_count += 1
                                hairpin_bool = True
                                break

                        hairpin_time_list.append(time.clock()-start_time)

                        if not hairpin_bool:

                            # tel x bij de locatie op als geschikte probe is gevonden en construct probe object
                            i += self.nucleotide_frame_skip

                            gene.probe_count += 1
                            probe_count += 1
                            fraction = (i+1) / len(gene.exon_seqs)

                            # Bepaling metlting temp (naive approach) niet accurate bij oligo nucs > 20
                            cur_tm = round((64.9 + 41 * (cur_g_count+cur_c_count-16.4)/(cur_a_count +
                                                                                        cur_t_count +
                                                                                        cur_g_count +
                                                                                        cur_c_count)), 3)

                            probes.append(Probes(i, cur_probe, fraction, cur_gc_perc, cur_tm))
                    else:

                        if skip_bool:
                            di_repeat_positions = di_search.span()
                            i += di_repeat_positions[0]
                            di_count += di_repeat_positions[0]
                        else:
                            i += 1
                            di_count += 1

                        di_time_list.append(time.clock()-start_time)
                else:

                    if skip_bool:
                        mono_repeat_positions = mono_search.span()
                        i += mono_repeat_positions[0]
                        mono_count += mono_repeat_positions[0]
                    else:
                        i += 1
                        di_count += 1

                    mono_time_list.append(time.clock()-start_time)
            else:
                gc_count += 1
                gc_time_list.append(time.clock() - start_time)

            i += 1

        # print('GENE ID:\t', gene.gene_id)
        # print('GC:\t\t\t',sum(gc_time_list))
        # print('MONO:\t\t',sum(mono_time_list))
        # print('DI:\t\t\t',sum(di_time_list))
        # print('HAIRPIN:\t', sum(hairpin_time_list))
        # print('TOTAL CALC: ', (sum(gc_time_list)+sum(mono_time_list)+sum(di_time_list)+sum(hairpin_time_list)))
        # print('TOTAL NORM: ', time.clock() - start_time_total)
        # print('----------------------------------------------')

        # TODO Figure out a proper way to set these
        gene.time_mono = sum(mono_time_list)
        gene.time_di = sum(di_time_list)
        gene.time_hairpin = sum(hairpin_time_list)
        gene.time_gc = sum(gc_time_list)
        gene.time_total = time.clock() - start_time_total

        gene.possible_probe_count = possible_probe_count
        gene.probe_count = probe_count
        gene.mono_count = mono_count
        gene.di_count = di_count
        gene.hairpin_count = hairpin_count
        gene.gc_count = gc_count

        return probes


class Probes:

    def __init__(self, probe_id, sequence, fraction, gc_perc, melting_temp):
        self.probe_id = probe_id
        self.sequence = sequence
        self.fraction = fraction
        self.gc_perc = gc_perc
        self.temp_melt = melting_temp


# import genbank_parser
# import glob
# import os
# import database_functions
# import exceptions
# def main():
#     start_time = time.clock()
#
#     # Set the settings for probe creation
#     nr_nuc_mono_repeat = 3
#     nr_nuc_di_repeat = 2
#     probe_length = 20
#     nucleotide_frame_skip = 0
#     min_gc_percentage = 20
#
#     prober = Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
#                     nr_nuc_mono_repeat=nr_nuc_mono_repeat,
#                     probe_length=probe_length,
#                     nucleotide_frame_skip=nucleotide_frame_skip,
#                     min_gc_percentage=min_gc_percentage)
#
#     chromosome_list = list()
#
#     # loop over gbk files genbank dir
#     for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):
#         # read genbank file
#
#         try:
#             genbank = genbank_parser.GenBank(filename=file)
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the genbank obj")
#             exit(-1)
#
#         try:
#             chromosome = genbank.make_chromosome()
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the chromosome obj")
#             exit(-1)
#
#         try:
#             chromosome.genes = genbank.make_genes()
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the gene obj")
#             exit(-1)
#         p_list = []
#         for gene in chromosome.genes:
#             gene.probes = prober.make_probes(gene)
#             p_list.append(len(gene.probes))
#         chromosome_list.append(chromosome)
#         print('Done with chromsome:', chromosome.chromosome_id)
#
#     # open a DB connection
#     database = database_functions.Database()
#     database.open_connection()
#     database.set_globals(False)
#
#     # set data to DB
#     database.set_probe_experiment(prober)
#     for chromosome in chromosome_list:
#         database.set_chromosome(chromosome)
#         print('Chromosome set to DB:', chromosome.chromosome_id)
#
#         for gene in chromosome.genes:
#             database.set_gene(gene, chromosome.chromosome_id)
#             database.set_probes(prober, gene)
#         print('Genes set to DB:', chromosome.chromosome_id)
#         print('Probes set to DB:', chromosome.chromosome_id)
#
#     database.set_globals(True)
#     database.close_connection()
#
#     print(time.clock()-start_time)
#
#
# if __name__ == '__main__':
#     # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
#     main()
