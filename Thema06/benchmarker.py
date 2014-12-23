#!/usr/bin/env python3
import genbank_parser
import glob
import prober
import os
import database_functions
import exceptions


def main():

    # Set the settings for probe creation
    nr_nuc_mono_repeat = 3
    nr_nuc_di_repeat = 2
    probe_length = 20
    nucleotide_frame_skip = 20
    min_gc_percentage = 60

    prober_obj = prober.Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                               nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                               probe_length=probe_length,
                               nucleotide_frame_skip=nucleotide_frame_skip,
                               min_gc_percentage=min_gc_percentage)

    chromosome_list = list()

    # open a DB connection
    database = database_functions.Database()
    database.open_connection()
    database.set_globals(False)

    # set data to DB
    pc_name = 'Desktop_1'
    proc_id = "i72600k"
    clockspeed = '3,4ghz'
    core_count = 4
    ram_size = 8
    arch = 'x86'
    inval_nuc_frame_skip = True
    comments = 'test'

    pc_id = database.set_benchmark_computers(pc_name, proc_id, clockspeed, core_count, ram_size, arch)
    bench_id = database.set_benchmark_benchmarks(prober_obj, inval_nuc_frame_skip, pc_id, comments)

    # loop over gbk files genbank dir
    for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):

        try:
            genbank = genbank_parser.GenBank(filename=file)
        except exceptions.ParseException:
            print("something went wrong in the creation of the genbank obj")
            exit(-1)

        try:
            chromosome = genbank.make_chromosome()
        except exceptions.ParseException:
            print("something went wrong in the creation of the chromosome obj")
            exit(-1)

        try:
            chromosome.genes = genbank.make_genes()
        except exceptions.ParseException:
            print("something went wrong in the creation of the gene obj")
            exit(-1)

        cur_gb_id = database.set_benchmark_genbank(bench_id, file, chromosome.chromosome_id)

        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene)
            database.set_benchmark_times(gene, cur_gb_id)

        chromosome_list.append(chromosome)
        print('Done with chromsome:', chromosome.chromosome_id)

    database.set_globals(True)
    database.close_connection()

if __name__ == '__main__':
    # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
    main()
