#!/usr/bin/env python3
"""
Author's: Olivier Bakker and Harm Brugge

Usage:
    -i      input folder
    -o      output folder
    [-oc]   Number of output files                  default = 1
    [-mr]   Maximum number of mono repeats          default = 3
    [-dr]   Maximum N=number of di repeats          default = 2
    [-l]    Length of the probe                     default = 20
    [-gc]   Minimum gc percentage                   default = 50%
    [-fs]   Skip a number of nucleotides            default = 0
    [-rs]   Skip to the end of a repeat region      default = True

File extension must be .gbk

"""
import genbank_parser
import glob
import prober
import os
import sys
import time
import database_functions
import argparse


def handler(input_folder, output_folder, number_of_files, nr_nuc_mono_repeat, nr_nuc_di_repeat, probe_length,
            nucleotide_frame_skip, min_gc_percentage, inval_nuc_frame_skip, database_bool):

    prober_obj = prober.Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
                               nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                               probe_length=probe_length,
                               nucleotide_frame_skip=nucleotide_frame_skip,
                               min_gc_percentage=min_gc_percentage)

    if database_bool:
        #open a DB connection
        database = database_functions.Database()
        database.open_connection()
        database.set_globals(False)
        database.set_probe_experiment(prober_obj)

    probe_list = list()
    file_iter = 1

    for file in glob.glob(os.path.join(input_folder, '*.gbk')):

        print('-'*80)
        print('[file] Number: ', file_iter, '\n[path] ',  file)

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()

        if database_bool:
            database.set_chromosome(chromosome)

        gene_len = len(chromosome.genes)
        gene_count = 0

        for gene in chromosome.genes:
            gene.probes = prober_obj.make_probes(gene, inval_nuc_frame_skip)
            probe_list += gene.probes

            if database_bool:
                database.set_gene(gene, chromosome.database_id)
                database.set_probes(prober_obj, gene)

            gene_perc = (gene_count/gene_len) * 100
            sys.stdout.write('\r[busy] {0}% [{1}{2}]'.format(round(gene_perc),
                                                             '='*(int(gene_perc/2.5)),
                                                             ' '*(int(40-(gene_perc/2.5)))))
            sys.stdout.flush()
            gene_count += 1

        print('\n[done]', file.split('/')[-1])
        file_iter += 1

    try:
        print('-'*80)
        genbank_parser.FastaWriter().write_probes_gondor(probe_list,
                                                         number_of_files,
                                                         output_folder)
    except OSError as e:
        print(e)
        exit(-1)

    if database_bool:
        database.commit()
        database.set_globals(True)
        database.close_connection()


def get_args():

    description_string = "Author's: Harm Brugge and Olivier Bakker\n"\
                         "Description: This program creates probes from .gbk files."
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=description_string)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-i', help='input folder', type=str)
    parser.add_argument('-o', help='output folder', type=str)
    parser.add_argument('-oc', help='Number of output files', type=int, default=1)
    parser.add_argument('-mr', help='Maximum number of mono repeats', type=int, default=3)
    parser.add_argument('-dr', help='Maximum number of di repeats', type=int, default=2)
    parser.add_argument('-l', help='Length of the probes', type=int, default=20)
    parser.add_argument('-gc', help='Minimum gc percentage', type=float, default=50.0)
    parser.add_argument('-fs', help='Skip a number of nucleotides after each probe', type=int, default=0)
    parser.add_argument('-rs', help='Skip to the end of repeat region', type=bool, default=True)
    parser.add_argument('-db', help='Save the data to the database', type=bool, default=False)
    args = parser.parse_args()

    if not args.i:
        parser.error('[ERROR] No input folder defined. Define one with -i <path/to/folder>')

    return args


def main():
    args = get_args()
    # Set the settings for probe creation

    print('+', '-'*74, '+')
    print('|', 'Probe designer'.center(74), '|')
    print('+', '-'*74, '+')

    if os.path.exists(args.o):

        print('[WARNNG] Folder '+args.o+' exists or is invalid')
        warning = input('Do you want to continue? y/n: ')
        if warning.lower() == 'n':
            exit(0)

    main_start_time = time.clock()
    handler(nr_nuc_mono_repeat=args.mr,
            nr_nuc_di_repeat=args.dr,
            probe_length=args.l,
            nucleotide_frame_skip=args.fs,
            min_gc_percentage=args.gc,
            input_folder=args.i,
            output_folder=args.o,
            number_of_files=args.oc,
            database_bool=args.db,
            inval_nuc_frame_skip=args.fs)

    print('-'*80)
    print('[Total elapsed] ', round((time.clock()-main_start_time), 3))

if __name__ == '__main__':
    main()
