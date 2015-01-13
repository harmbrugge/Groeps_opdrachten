# import genbank_parser
# import glob
# import os
# import database_functions
# import exceptions
# def main():
#     start_time = time.clock()
#
#     # Set the settings for probe creation
#     nr_nuc_mono_repeat = 3
#     nr_nuc_di_repeat = 2
#     probe_length = 20
#     nucleotide_frame_skip = 0
#     min_gc_percentage = 20 SELECT oligo_id FROM th6_blasts WHERE alignment_len = 20 GROUP BY oligo_id HAVING count(*) = 1
#
#     prober = Prober(nr_nuc_di_repeat=nr_nuc_di_repeat,
#                     nr_nuc_mono_repeat=nr_nuc_mono_repeat,
#                     probe_length=probe_length,
#                     nucleotide_frame_skip=nucleotide_frame_skip,
#                     min_gc_percentage=min_gc_percentage)
#
#     chromosome_list = list()
#
#     # loop over gbk files genbank dir
#     for file in glob.glob(os.path.join('genbank_files/Plasmodium', '*.gbk')):
#         # read genbank file
#
#         try:
#             genbank = genbank_parser.GenBank(filename=file)
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the genbank obj")
#             exit(-1)
#
#         try:
#             chromosome = genbank.make_chromosome()
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the chromosome obj")
#             exit(-1)
#
#         try:
#             chromosome.genes = genbank.make_genes()
#         except exceptions.ParseException:
#             print("something went wrong in the creation of the gene obj")
#             exit(-1)
#         p_list = []
#         for gene in chromosome.genes:
#             gene.probes = prober.make_probes(gene)
#             p_list.append(len(gene.probes))
#         chromosome_list.append(chromosome)
#         print('Done with chromsome:', chromosome.chromosome_id)
#
#     # open a DB connection
#     database = database_functions.Database()
#     database.open_connection()
#     database.set_globals(False)
#
#     # set data to DB
#     database.set_probe_experiment(prober)
#     for chromosome in chromosome_list:
#         database.set_chromosome(chromosome)
#         print('Chromosome set to DB:', chromosome.chromosome_id)
#
#         for gene in chromosome.genes:
#             database.set_gene(gene, chromosome.chromosome_id)
#             database.set_probes(prober, gene)
#         print('Genes set to DB:', chromosome.chromosome_id)
#         print('Probes set to DB:', chromosome.chromosome_id)
#
#     database.set_globals(True)
#     database.close_connection()
#
#     print(time.clock()-start_time)
#
#
# if __name__ == '__main__':
#     # C:\"Program Files (x86)"\"Windows Resource Kits"\Tools\timeit C:\python34\python prober.py
#     main()
