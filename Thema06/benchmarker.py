0#!/usr/bin/env python3
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

    # open a DB connection
    database = database_functions.Database()
    database.open_connection()
    database.set_globals(False)

    database.set_probe_experiment(prober_obj)

    for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()

        database.set_chromosome(chromosome)

        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene, inval_nuc_frame_skip)
            database.set_gene(gene, chromosome.chromosome_id)
            database.set_probes(prober_obj, gene)

        database.commit()
        print('[done] ', file)

    database.set_globals(True)
    database.close_connection()


def main():


    # Set the settings for probe creation
    main_start_time = time.clock()
    handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=0, min_gc_percentage=20)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
          round((time.clock()-main_start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 20, 0, 20, False, 'inval nuc skip off 20%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 20, 0, 50, True, 'inval nuc skip on 50%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 20, 0, 50, False, 'inval nuc skip off 50%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 25, 0, 50, True, 'inval nuc skip on 50%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 30, 0, 50, True, 'inval nuc skip on 50%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))
    # start_time = time.clock()
    #
    # handler(3, 2, 35, 0, 50, True, 'inval nuc skip on 50%')
    # print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',
    #       round((time.clock()-start_time), 3))


if __name__ == '__main__':
    # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
    main()
