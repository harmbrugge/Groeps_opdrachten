#!/usr/bin/env python3
import genbank_parser
import glob
import prober
import os
import sys
import time
import database_functions
import exceptions


def main():

    # version = sys.version_info
    # # Reqeuest the pc data from the user.
    # print('+------------------------------------------------------+')
    # python_verison = ''.join([str(version.major), str(version.minor), str(version.micro), str(version.releaselevel)])
    # pc_name = input('Enter the pc name: ')
    # proc_id = input('Enter the proccesor name: ')
    # arch = input('Enter the proccesors architecture: ')
    # clockspeed = input('Enter the proccesors clockspeed: ')
    # core_count = input('Enter the proccesors core count: ')
    # ram_size = input('Enter the coumputers ram size: ')
    # ram_speed = input('Enter the coumputers ram speed: ')
    # operating_sytem = input('Enter the coumputers operating system: ')
    # kernel_version = input('Enter the coumputers operating systems kernel version: ')
    # print('+------------------------------------------------------+')

    pc_name = 'Desktop_1'
    proc_id = "i72600k"
    clockspeed = 3400
    core_count = 4
    ram_size = 8
    arch = 'x86'
    ram_speed = 1366
    python_verison = '3.4.1'
    operating_sytem = 'Microsoft windows 8'
    kernel_version = 'Some kernal'
    inval_nuc_frame_skip = True
    comments = 'test'

    # open a DB connection
    database = database_functions.Database()
    database.open_connection()
    database.set_globals(False)

    pc_id = database.set_benchmark_computers(pc_name,
                                             proc_id,
                                             clockspeed,
                                             core_count,
                                             ram_size,
                                             ram_speed,
                                             arch,
                                             python_verison,
                                             operating_sytem,
                                             kernel_version)

    benchmarks = {}

    # Set the settings for probe creation
    nr_nuc_mono_repeat = 3
    nr_nuc_di_repeat = 2
    probe_length = 20
    nucleotide_frame_skip = 0
    min_gc_percentage = 20

    prober_obj = prober.Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                               nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                               probe_length=probe_length,
                               nucleotide_frame_skip=nucleotide_frame_skip,
                               min_gc_percentage=min_gc_percentage)

    chromosome_list = list()

    bench_id = database.set_benchmark_benchmarks(prober_obj, inval_nuc_frame_skip, pc_id, comments)

    # loop over gbk files genbank dir
    time_lst  = []
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
        start_time = time.clock()
        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene, inval_nuc_frame_skip)
            #database.set_benchmark_times(gene, cur_gb_id)
        time_lst.append(time.clock()-start_time)

        chromosome_list.append(chromosome)
        print('Done with chromsome:', chromosome.chromosome_id)

    print(sum(time_lst))
    database.set_globals(True)
    database.close_connection()

if __name__ == '__main__':
    # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
    main()
