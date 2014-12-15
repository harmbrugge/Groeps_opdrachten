#!/usr/bin/env python3
import pymysql
import re
import datetime


class Main():
    """
    Couldn't think of a better name than main so it will have to do for now.
    this class contains methods used for opening the config file and sanatizing
    the sql input.
    """

    @staticmethod
    def sanitize_input(query):
        """
        This method helps prevent sql injection. It uses regex to do this.
        :param: The input 'query'
        :return: A boolean wich is true if sql is detected in the query.
        """
        # TODO fix the regex for sql so that things like .or. dont pickup stuff

        forbidden_sql = '\sor\s|\'or.|\sand\s|\'and.|\sdrop\s|\'drop.|.;.|.;|\s;\s'
        if re.search(forbidden_sql, query.lower()):
            injection_bool = True
        else:
            injection_bool = False
        # TODO expand this method so the protection is better/more versitile
        return injection_bool

    @staticmethod
    def get_database_login_data(filename='config.my.cnf'):
        """
        This function gets the connection data from the config file.
        :param filename: The name/path of the configfile
        :return: If no errors ouccurd a list containing login data is returned
        """

        try:
            config_file = open(filename, 'r')

            try:
                # The regular expressions for getting the connection data.
                data = ''.join(config_file.readlines())
                password = re.search('\[user\]\s(.*\s)*password\s?=\s?(.*)', data).group(2)
                user = re.search('\[user\]\s(.*\s)*user\s?=\s?(.*)', data).group(2)
                host = re.search('\[host\]\s(.*\s)*hostname\s?=\s?(.*)', data).group(2)
                database = re.search('\[database\]\s(.*\s)*database_name\s?=\s?(.*)', data).group(2)
                config_file.close()
                return [password, user, host, database]

            except AttributeError:
                # If the config file is not created according to the proper standards an entry in the logfile is made.
                error_log = open('error_log_databases_2.log', 'a')
                error_log.write(str(datetime.datetime.now()) + ': An error ouccurd in database_functions.py TYPE ERROR:'
                                                               ' IncorrectConfigFileError\n')
                error_log.close()

        except (OSError, IOError):
            # If the configfile is not present an entry in the logfile is made.
            error_log = open('error_log_databases_2.log', 'a')
            error_log.write(str(datetime.datetime.now()) + ': An error ouccurd in database_functions.py TYPE ERROR:'
                                                           ' FileNotFounError\n')
            error_log.close()

        # TODO create a class/module desinged for handeling the errors insted of doing it this way
            # TODO make the error logging more 'dynamic' and not just printing a string.


class Dynamic():

    def __init__(self):
        self.connection = None
        self.cursor = None

    def get_cursor(self):
        """
        Get the cursor object.
        """
        # TODO perhaps make a database 'superclass' containing get/close cursor methods
        connection_data = Main.get_database_login_data()
        self.connection = pymysql.connect(host=connection_data[2],
                                          database=connection_data[3],
                                          user=connection_data[1],
                                          passwd=connection_data[0])

        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def close_cursor(self):
        """
        Close the cursor object.
        """
        self.connection.close()
        self.cursor.close()

    def set_chromosome(self, chromosome_obj):

        self.cursor.execute('insert into th6_chromosome (organism, chromosome_def) '
                            'values ("{0}", "{1}");'.format(chromosome_obj.organism,
                                                            chromosome_obj.chromosome_id))
        self.connection.commit()
        chromosome_obj.chromosome_id = self.connection.insert_id()

    def set_gene(self, gene_obj):

        self.cursor.execute('insert into th6_gene (chromosome_id,'
                                                  'external_id,'
                                                  'sequence,'
                                                  'strand,'
                                                  'protein,'
                                                  'protein_id)'
                            'values ("{0}", "{1}", "{2}", "{3}", "{4}", "{5}");'.format(gene_obj.chromosome_id,
                                                                                        gene_obj.gene_id,
                                                                                        gene_obj.sequence,
                                                                                        gene_obj.strand,
                                                                                        gene_obj.protein,
                                                                                        gene_obj.protein_id))
        self.connection.commit()



