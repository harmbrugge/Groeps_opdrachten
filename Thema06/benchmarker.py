#!/usr/bin/env python3
import genbank_parser
import glob
import prober
import os
import sys
import time
import database_functions


def handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=50,
            inval_nuc_frame_skip=True):

    prober_obj = prober.Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                               nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                               probe_length=probe_length,
                               nucleotide_frame_skip=nucleotide_frame_skip,
                               min_gc_percentage=min_gc_percentage)

    #open a DB connection
    #database = database_functions.Database()
    #database.open_connection()
    #database.set_globals(False)

   # database.set_probe_experiment(prober_obj)
    probe_list = list()
    file_iter = 1

    for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):

        print('[file] number: ', file_iter, ' path: ',  file)

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()

        #database.set_chromosome(chromosome)
        gene_len = len(chromosome.genes)
        gene_count = 0
        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene, inval_nuc_frame_skip)
            probe_list += gene.probes
            #database.set_gene(gene, chromosome.database_id)
            #database.set_probes(prober_obj, gene)

            gene_perc = (gene_count/gene_len) * 100
            sys.stdout.write('\r[busy] genes: {0}'.format(round(gene_perc, 3)))
            sys.stdout.flush()
            gene_count += 1

        #database.commit()
        print('\n[done] ', file)
        file_iter += 1

    genbank_parser.FastaWriter().write_probes_gondor(probe_list, 50,
                                                     '/commons/student/2014-2015/Thema06/harm_olivier/Experiment_'
                                                     + str(prober_obj.id) + '/in/')

    #database.set_globals(True)
    #database.close_connection()


def main():

    # Set the settings for probe creation
    main_start_time = time.clock()
    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=20)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=30)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=40)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=50)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=25, nucleotide_frame_skip=0, min_gc_percentage=20)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=25, nucleotide_frame_skip=0, min_gc_percentage=30)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=25, nucleotide_frame_skip=0, min_gc_percentage=40)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=25, nucleotide_frame_skip=0, min_gc_percentage=50)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=30, nucleotide_frame_skip=0, min_gc_percentage=20)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=30, nucleotide_frame_skip=0, min_gc_percentage=30)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=30, nucleotide_frame_skip=0, min_gc_percentage=40)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=30, nucleotide_frame_skip=0, min_gc_percentage=50)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))

if __name__ == '__main__':
    # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
    main()
