#!/usr/bin/env python3
import pymysql
import re
import prober
from genbank_parser import Gene, Chromosome, FastaWriter
import time


class Database:
    """
    Database class manages the connection and
    data transfer to and from MySQL Server
    """

    def __init__(self):
        config = self._get_configurations()
        self.host = config["host"]
        self.user = config["user"]
        self.passwd = config["passwd"]
        self.db = config["db"]
        self.conn = None
        self.cur = None

    @staticmethod
    def _get_configurations():
        config_info = dict()

        file = open('my.cnf', 'r')

        for line in file:
            if re.search('(.=.)', line):
                line = line.strip('\n')
                line = line.split('=')
                config_info.update({line[0]: line[1]})

        return config_info

    def open_connection(self):
        """
        Opens a connection required for any other operation
        """
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db)
        self.cur = self.conn.cursor()

    def close_connection(self):
        """
        Close the connection after you're done
        """
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def set_globals(self, bool):
        """
        Used for major import operations.
        :param bool:
        :return:
        """

        if bool:
            self.cur.execute('SET autocommit = 1')
            self.cur.execute('SET foreign_key_checks = 1;')
            self.cur.execute('SET unique_checks=1;')
        else:
            self.cur.execute('SET autocommit = 0')
            self.cur.execute('SET foreign_key_checks = 0;')
            self.cur.execute('SET unique_checks=0;')

    def set_chromosome(self, chromosome_obj):
        # Use only first two words in organism name for database entry (not bullet proof)
        chromosome_obj.organism = re.search('([^\s]+\s+[^\s]+)', chromosome_obj.organism).group(1)

        # Search if the organism naam exists in database
        self.cur.execute('SELECT id FROM th6_organism WHERE name = "{0}"'.format(chromosome_obj.organism))
        organism_id = self.cur.fetchone()

        # If exists use the id for insert in DB, else create new organism entry
        if organism_id:
            chromosome_obj.organism_id = organism_id[0]
        else:
            self.cur.execute('INSERT INTO th6_organism (name) VALUE ("{0}")'.format(chromosome_obj.organism))
            chromosome_obj.organism_id = self.conn.insert_id()

        # Insert chromsome into to DB
        self.cur.execute('INSERT INTO th6_chromosome (organism_id, organism, chromosome_def) '
                         'VALUES ("{0}", "{1}", "{2}");'.format(chromosome_obj.organism_id,
                                                                chromosome_obj.organism,
                                                                chromosome_obj.chromosome_id))
        # self.conn.commit()
        chromosome_obj.chromosome_id = self.conn.insert_id()

    def set_gene(self, gene_obj, chromosome_id):

        self.cur.execute('INSERT INTO th6_gene (chromosome_id,'
                         'external_id,'
                         'sequence,'
                         'strand,'
                         'protein,'
                         'protein_id)'
                         'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");'.format(chromosome_id,
                                                                                     gene_obj.gene_id,
                                                                                     gene_obj.exon_seqs,
                                                                                     gene_obj.strand,
                                                                                     gene_obj.protein,
                                                                                     gene_obj.protein_id))
        gene_obj.db_id = self.conn.insert_id()

        # self.conn.commit()
    def set_probe_experiment(self, prober):
        self.cur.execute(
            'INSERT INTO th6_probe_experiment '
            '(date, '
            'set_mono_repeat, '
            'set_di_repeat, '
            'set_coverage, '
            'set_probe_len, '
            'count_mono_repeat, '
            'count_di_repeat, '
            'count_hairpin,'
            'count_possible,'
            'count_total,'
            'count_gc,'
            'time_total) '
            'VALUES (NULL, {0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})'.format(prober.nr_nuc_mono_repeat,
                                                                                prober.nr_nuc_di_repeat,
                                                                                prober.coverage,
                                                                                prober.probe_length,
                                                                                prober.mono_count,
                                                                                prober.di_count,
                                                                                prober.hairpin_count,
                                                                                prober.possible_probe_count,
                                                                                prober.probe_count,
                                                                                prober.gc_count,
                                                                                prober.time_total))
        # get the inserted primary key, needed for fk oligo table
        prober.id = self.conn.insert_id()

    def set_probes(self, prober, gene):

        for probe in gene.probes:

            self.cur.execute('INSERT INTO th6_oligo (gene_id, '
                             'probe_experiment_id, '
                             'sequence, '
                             'fraction,'
                             'cg_perc) '
                             'VALUES ({0}, {1}, "{2}", {3}, {4})'.format(gene.db_id,
                                                                    prober.id,
                                                                    probe.sequence,
                                                                    probe.fraction,
                                                                    probe.gc_perc))
            probe.probe_id = self.conn.insert_id()

        self.cur.execute('INSERT INTO th6_experiment_genes ('
                         'th6_gene_id, '
                         'th6_probe_experiment_id, '
                         'count_mono_repeat, '
                         'count_di_repeat, '
                         'count_hairpin, '
                         'count_possible, '
                         'count_total,'
                         'count_gc,'
                         'time_mono,'
                         'time_di,'
                         'time_hairpin,'
                         'time_total,'
                         'time_gc) '
                         'VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})'.format(gene.db_id,
                                                                             prober.id,
                                                                             gene.mono_count,
                                                                             gene.di_count,
                                                                             gene.hairpin_count,
                                                                             gene.possible_probe_count,
                                                                             gene.probe_count,
                                                                             gene.gc_count,
                                                                             gene.time_mono,
                                                                             gene.time_di,
                                                                             gene.time_hairpin,
                                                                             gene.time_total,
                                                                             gene.time_gc))

    def get_chromomes(self):
        self.cur.execute('SELECT * FROM th6_chromosome')
        chromosome_list = list()

        for row in self.cur.fetchall():
            chromosome_list.append(Chromosome('', row[0], row[3]))

        return chromosome_list

    def get_genes(self, chromosome):
        self.cur.execute('SELECT * FROM th6_gene WHERE chromosome_id = "{0}"'.format(chromosome.chromosome_id))
        for row in self.cur.fetchall():
            chromosome.genes.append(Gene(row[0], row[6], None, row[3], row[7], row[8], chromosome))

    def get_probes(self, gene):
        self.cur.execute('SELECT * FROM th6_oligo WHERE gene_id = "{0}"'.format(gene.gene_id))
        for row in self.cur.fetchall():
            pass
            gene.probes.append(prober.Probes(row[0], row[3], row[6]))

if __name__ == '__main__':
    start_time = time.time()

    db = Database()
    db.open_connection()

    fastawriter = FastaWriter()

    probe_list = list()

    chromosomes = db.get_chromomes()
    for chrom in chromosomes:
        db.get_genes(chrom)
        for gen in chrom.genes:
            db.get_probes(gen)

    for chrom in chromosomes:
        probe_list.append(fastawriter.get_probe_string(chrom.genes))

    fastawriter.write_list(probe_list)

    db.close_connection()

    print(time.time()-start_time)

# C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py