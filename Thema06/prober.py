#!/usr/bin/env python3
import genbank_parser
import re
import glob
import os
import datetime
import database_functions
import sys


class Prober:

    def __init__(self):

        self.trans_table = str.maketrans("atcg", "tagc")

    def make_probes(self, gene, nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):

        i = 0

        probes = list()

        while i < len(gene.exon_seqs) - probe_length:
            gene.possible_probe_count += 1
            cur_probe = gene.exon_seqs[i:i+probe_length]

            # Zoek naar 4-nuc-mono-repeats
            nuc_mono_repeat = '(\w)\\1{' + str(nr_nuc_mono_repeat) + '}'
            nuc_di_repeat = '(\w{2,3})\\1{' + str(nr_nuc_di_repeat) + '}'

            if not re.search(nuc_mono_repeat, cur_probe):
                # Zoek naar 3-nuc-di-repeats
                if not re.search(nuc_di_repeat, cur_probe):

                    # Pak alleen het gebied na 5(hairpin sequentie) + 3(gap)
                    hairpin_domain = cur_probe[8:]
                    hairpin_bool = False

                    # Pak alle mogelijke sequenties van 5 in hairpin_domain
                    for y in range(0, len(hairpin_domain)-5):
                        hairpin_seq = hairpin_domain[y:y+5]

                        # Maak de sequenties reverse complement
                        hairpin_seq_rev_com = hairpin_seq.translate(self.trans_table)[::-1]

                        # Zoek op de probe naar de sequentie rekening houdend met eindlocatie
                        if hairpin_seq_rev_com in cur_probe[:y+5]:
                            gene.hairpin_count += 1
                            hairpin_bool = True
                            break

                    if not hairpin_bool:
                        # tel 10 locatie op als geschikte probe is gevonden en construct probe object
                        i += coverage
                        gene.probe_count += 1
                        fraction = (i+1) / len(gene.exon_seqs)

                        probes.append(Probes(i, cur_probe, fraction))
                else:
                    gene.di_count += 1
            else:
                gene.mono_count += 1

            i += 1
        return probes


class Probes:

    def __init__(self, probe_id, sequence, fraction):
        self.probe_id = probe_id
        self.sequence = sequence
        self.fraction = fraction


class Handler:

    @staticmethod
    def handler(nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10):
        # 1:34 met db cursor broken
        # 1:02 zonder db
        # 1:02 met db cursor fixed
        # 1:04 met db cursor fixed
        # Set the parameters for the probe construction. TODO make these user configurable via gci

        gene_list = list()
        prober = Prober()
        database = database_functions.Dynamic()
        database.get_cursor()

        # TODO construct a prober id based on something unique (other than a time)
        session_id = 'SESSION TEST|' + str(datetime.datetime.now())

        # Add session entry to db.
        database.set_data('sessions', ['session_id',
                                       'date'], [session_id,
                                                 str(datetime.datetime.now())])

        # Add the parameters to the database.
        database.set_data('settings', ['mono_repeat',
                                       'di_repeat',
                                       'probe_len',
                                       'covarage',
                                       'sessions_session_id'], [str(nr_nuc_mono_repeat),
                                                                str(nr_nuc_di_repeat),
                                                                str(probe_length),
                                                                str(coverage),
                                                                str(session_id)])

        # Loop over the genbank Files
        for file in glob.glob(os.path.join('genbank_files/', '*.gbk')):

            # Get the current time.
            start_time = datetime.datetime.now()

            # Construct gene and chromosome objects.
            genbank = genbank_parser.GenBank(filename=file)
            chromosome = genbank.make_chromosome()
            chromosome.genes = genbank.make_genes()

            # Get the fasta file string for the gene objects.
            cur_gene_list = genbank_parser.FastaWriter.get_gene_string(chromosome.genes)
            gene_list.append(cur_gene_list)

            # Initialize the counters.
            possible_probe_count = 0
            probe_count = 0
            mono_count = 0
            di_count = 0
            hairpin_count = 0

            # Constuct an id for the database. TODO make this better so its always unique
            cur_chromosome = 'chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism)

            # Set the chromome table. TODO add the time and size param's
            database.set_data('chromosomes', ['chromosome_id',
                                              'gene_count',
                                              'sessions_session_id'], [str(cur_chromosome),
                                                                       str(len(chromosome.genes)),
                                                                       str(session_id)])
            # Loop over the genes in the chromosome.
            for gene in chromosome.genes:
                # Construct the probes.
                gene.probes = prober.make_probes(gene,
                                                 nr_nuc_mono_repeat=nr_nuc_mono_repeat,
                                                 nr_nuc_di_repeat=nr_nuc_di_repeat,
                                                 probe_length=probe_length,
                                                 coverage=coverage)

                # Append the values from eacht gene to the counter defined above.
                possible_probe_count += gene.possible_probe_count
                probe_count += gene.probe_count
                mono_count += gene.mono_count
                di_count += gene.di_count
                hairpin_count += gene.hairpin_count

            # Set the probe data in the database.
            database.set_data('discarded_probes', ['count_total',
                                                   'count_valid_probes',
                                                   'count_mono_repeat',
                                                   'count_di_repeat',
                                                   'count_hairpin',
                                                   'chromosomes_chromosome_id'], [str(possible_probe_count),
                                                                                  str(probe_count),
                                                                                  str(mono_count),
                                                                                  str(di_count),
                                                                                  str(hairpin_count),
                                                                                  str(cur_chromosome)])

            # Calculate the time it took to make the probes and parse the file.
            exec_time = (datetime.datetime.now()-start_time)
            gb_obj_size = sys.getsizeof(genbank.file_string)

            print(exec_time, ';', gb_obj_size)
            # Write the fasta files.
            probe_list = genbank_parser.FastaWriter.get_probe_string(chromosome.genes)
            genbank_parser.FastaWriter.write(probe_list)

        # Close the cursor object.
        database.close_cursor()

        # Make the gene fasta file.
        genbank_parser.FastaWriter.write_list(gene_list)


def main():
    Handler().handler()


if __name__ == '__main__':
    main()
    #C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit timeit C:\python34\python prober.py