#!/usr/bin/env python3
"""
Author's: Olivier Bakker and Harm Brugge

Usage:
    -i      input folder
    -o      output folder
    -f      filename

File extension must be .gbk
"""
import genbank_parser
import glob
import os
import sys
import time
import argparse


def handler(input_folder, output_folder, filename):

    file_iter = 1
    gene_strings = []
    number_of_files = len(glob.glob(os.path.join(input_folder, '*.gbk')))
    if number_of_files < 1:
        print('no valdid shizzle found!')
    fasta_writer = genbank_parser.FastaWriter()

    for file in glob.glob(os.path.join(input_folder, '*.gbk')):

        print('-'*80)
        print('[file] Number: ',
              file_iter, '[size]',
              round((os.path.getsize(file)/1000000), 2),
              'Mb\n[path] ',  file)

        genbank = genbank_parser.GenBank(filename=file)
        chromosome = genbank.make_chromosome()
        chromosome.genes = genbank.make_genes()
        cur_gene_string = fasta_writer.get_gene_string(chromosome.genes)
        gene_strings.append(cur_gene_string[0])

        perc = (file_iter/number_of_files) * 100
        sys.stdout.write('\r[busy] {0}% [{1}{2}]'.format(round(perc),
                                                         '='*(int(perc/2.5)),
                                                         ' '*(int(40-(perc/2.5)))))
        sys.stdout.flush()
        file_iter += 1
        print('\n[done]', file.split('/')[-1])

    try:
        print('-'*80)
        fasta_writer.write([gene_strings, filename], output_folder)

    except OSError as e:
        print(e)
        exit(-1)



def get_args():

    description_string = "Author's: Harm Brugge and Olivier Bakker\n"\
                         "Description: This program creates a single gene fasta from .gbk files."
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=description_string)

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-i', help='Input folder', type=str)
    parser.add_argument('-o', help='Output folder', type=str)
    parser.add_argument('-f', help='Filename', type=str)
    args = parser.parse_args()

    if not args.i:
        parser.error('[ERROR] No input folder defined. Define one with -i <path/to/folder>')
    elif not args.o:
        parser.error('[ERROR] No output folder defined. Define one with -o <path/to/folder>')
    elif not args.f:
        parser.error('[ERROR] No filename defined. Define one with -f <filename>')

    return args


def main():
    args = get_args()
    # Set the settings for probe creation

    print('+', '-'*76, '+')
    print('|', 'Gene fasta writer'.center(76), '|')
    print('+', '-'*76, '+')

    if os.path.exists(args.o):
        print('[WARNNG] Folder '+args.o+' exists or is invalid')
        warning = input('Do you want to continue? y/n: ')
        if warning.lower() == 'n':
            exit(0)

    main_start_time = time.clock()
    handler(input_folder=args.i,
            output_folder=args.o,
            filename=args.f)

    print('-'*80)
    print('[Total time elapsed] ', round((time.clock()-main_start_time), 3))

if __name__ == '__main__':
    main()
