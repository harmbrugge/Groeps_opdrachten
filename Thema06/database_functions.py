#!/usr/bin/env python3
import pymysql
import re
import datetime


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
        self.cur = self.conn.cursor()
        self.conn.close()

    def set_chromosome(self, chromosome_obj):
        self.cur.execute('INSERT INTO th6_chromosome (organism, chromosome_def) '
                         'VALUES ("{0}", "{1}");'.format(chromosome_obj.organism,
                                                         chromosome_obj.chromosome_id))
        # self.conn.commit()
        chromosome_obj.chromosome_id = self.conn.insert_id()

    def set_gene(self, gene_obj):

        self.cur.execute('INSERT INTO th6_gene (chromosome_id,'
                         'external_id,'
                         'sequence,'
                         'strand,'
                         'protein,'
                         'protein_id)'
                         'VALUES ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");'.format(gene_obj.chromosome_id,
                                                                                     gene_obj.gene_id,
                                                                                     gene_obj.sequence,
                                                                                     gene_obj.strand,
                                                                                     gene_obj.protein,
                                                                                     gene_obj.protein_id))
        # self.conn.commit()


