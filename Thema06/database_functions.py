#!/usr/bin/env python3
import pymysql
import re
import prober
from genbank_parser import Gene, Chromosome


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

    def set_globals(self, check_bool):
        """
        Used for major import operations.
        :param check_bool:
        :return:
        """

        if check_bool:
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
        self.cur.execute('INSERT INTO th6_chromosomes (organism_id, organism, chromosome_def) '
                         'VALUES ("{0}", "{1}", "{2}");'.format(chromosome_obj.organism_id,
                                                                chromosome_obj.organism,
                                                                chromosome_obj.chromosome_id))

        chromosome_obj.chromosome_id = self.conn.insert_id()

    def set_gene(self, gene_obj, chromosome_id):

        self.cur.execute('INSERT INTO th6_genes (chromosome_id,'
                         'external_id,'
                         'strand,'
                         'protein,'
                         'protein_id)'
                         'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}");'.format(chromosome_id,
                                                                              gene_obj.gene_id,
                                                                              gene_obj.strand,
                                                                              gene_obj.protein,
                                                                              gene_obj.protein_id))
        # Removed the seqeunce for testing
        gene_obj.db_id = self.conn.insert_id()

    def set_probe_experiment(self, prober_obj):

        self.cur.execute('INSERT INTO th6_experiment_settings'
                         '(date, '
                         'set_mono_repeat, '
                         'set_di_repeat, '
                         'set_coverage, '
                         'set_probe_len,'
                         'set_min_gc_perc) '
                         'VALUES (NULL, {0}, {1}, {2}, {3}, {4})'.format(prober_obj.nr_nuc_mono_repeat,
                                                                         prober_obj.nr_nuc_di_repeat,
                                                                         prober_obj.coverage,
                                                                         prober_obj.probe_length,
                                                                         prober_obj.min_gc_percentage))
        # get the inserted primary key, needed for fk oligo table
        prober_obj.id = self.conn.insert_id()

    def set_probes(self, prober_obj, gene):

        for probe in gene.probes:

            self.cur.execute('INSERT INTO th6_oligos (gene_id, '
                             'experiment_id, '
                             'sequence, '
                             'fraction,'
                             'cg_perc,'
                             'temp_melt) '
                             'VALUES ({0}, {1}, "{2}", {3}, {4}, {5})'.format(gene.db_id,
                                                                              prober_obj.id,
                                                                              probe.sequence,
                                                                              probe.fraction,
                                                                              probe.gc_perc,
                                                                              probe.temp_melt))
            # Het pakken van de inserted primary key's kost veel tijd!
            probe.probe_id = self.conn.insert_id()

        self.cur.execute('INSERT INTO th6_gene_experiment_data ('
                         'gene_id, '
                         'experiment_id, '
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
                         'VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, '
                         '{7}, {8}, {9}, {10}, {11}, {12})'.format(gene.db_id,
                                                                   prober_obj.id,
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

    def set_valid_probes_from_blast(self):

        self.cur.execute('SELECT oligo_id FROM th6_blasted_oligos '
                         'WHERE alignment_len = 20 GROUP BY oligo_id HAVING count(*) = 1')

        for row in self.cur.fetchall():
            self.cur.execute('UPDATE th6_oligos SET blast = TRUE WHERE id = "{0}"'.format(row[0]))

    def start_transaction(self):
        self.cur.execute('start transaction;')

    def commit(self):
        self.cur.execute('commit;')

    def get_chromomes(self):

        self.cur.execute('SELECT * FROM th6_chromosomes')
        chromosome_list = list()

        for row in self.cur.fetchall():
            chromosome_list.append(Chromosome('', row[0], row[3]))

        return chromosome_list

    def get_genes(self, chromosome):

        self.cur.execute('SELECT * FROM th6_genes WHERE chromosome_id = "{0}"'.format(chromosome.chromosome_id))
        for row in self.cur.fetchall():
            chromosome.genes.append(Gene(row[0], row[6], None, row[3], row[7], row[8], chromosome))

    def get_probes(self, gene):

        self.cur.execute('SELECT * FROM th6_oligos WHERE gene_id = "{0}"'.format(gene.gene_id))
        for row in self.cur.fetchall():
            gene.probes.append(prober.Probes(row[0], row[3], row[6], row[4], row[5]))