#!/usr/bin/env python3
import genbank_parser
import glob
import prober
import os
import sys
import time
import database_functions


def handler(pc_id, database, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, nucleotide_frame_skip=2, min_gc_percentage=50,
            inval_nuc_frame_skip=True, comments='This is a stoch comment'):

    prober_obj = prober.Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                               nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                               probe_length=probe_length,
                               nucleotide_frame_skip=nucleotide_frame_skip,
                               min_gc_percentage=min_gc_percentage)

    #bench_id = database.set_benchmark_benchmarks(prober_obj, inval_nuc_frame_skip, pc_id, comments)

    for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()
        db_genbank = database.get_benchmark_genbank(file)

        if not db_genbank:
            pass
            #gb_id = database.set_benchmark_genbank(file, chromosome.chromosome_id)
        else:
            gb_id = db_genbank[0]

        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene, inval_nuc_frame_skip)
            #database.set_benchmark_times(gene, bench_id, gb_id)
        print('[done] ', file)

def main():
    # open a DB connection
    database = database_functions.Database()
    database.open_connection()
    database.set_globals(False)

    print('Availible machines: ')
    print('+------------------------------------------------------+')
    print('\n'.join(['|ID '+str(x[0])+' NAME: '+str(x[1]+'|') for x in database.get_benchmark_computers()]))
    print('+------------------------------------------------------+')
    a = input('Existing machine(1) or create one(0)?:  ')

    if a == '0':
        version = sys.version_info
        # Reqeuest the pc data from the user.
        print('+------------------------------------------------------+')
        python_verison = ''.join([str(version.major), str(version.minor), str(version.micro), str(version.releaselevel)])
        pc_name = input('Enter the pc name: ')
        proc_id = input('Enter the proccesor name: ')
        arch = input('Enter the proccesors architecture: ')
        clockspeed = input('Enter the proccesors clockspeed: ')
        core_count = input('Enter the proccesors core count: ')
        ram_size = input('Enter the coumputers ram size: ')
        ram_speed = input('Enter the coumputers ram speed: ')
        operating_sytem = input('Enter the coumputers operating system: ')
        kernel_version = input('Enter the coumputers operating systems kernel version: ')
        print('+------------------------------------------------------+')

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

    else:
        pc_id = input('Enter the id of the pc: ')

    # Set the settings for probe creation
    main_start_time = time.clock()
    handler(pc_id, database, 3, 2, 20, 0, 20, True, 'inval nuc skip on 20%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-main_start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 20, 0, 20, False, 'inval nuc skip off 20%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 20, 0, 50, True, 'inval nuc skip on 50%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 20, 0, 50, False, 'inval nuc skip off 50%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 25, 0, 50, True, 'inval nuc skip on 50%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 30, 0, 50, True, 'inval nuc skip on 50%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))
    start_time = time.clock()
    handler(pc_id, database, 3, 2, 35, 0, 50, True, 'inval nuc skip on 50%')
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3), ' [Iteration elapsed] ',round((time.clock()-start_time), 3))

    database.set_globals(True)
    database.close_connection()

if __name__ == '__main__':
    # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
    main()
