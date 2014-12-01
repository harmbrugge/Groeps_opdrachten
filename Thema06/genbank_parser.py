#!/usr/bin/env python3
import re
import os


class GenBank:

    def __init__(self, file):
        self.file_string = str()
        self.file = file
        self._read_file()
        self.chromosome = None
        self.genes = None

    def __str__(self):
        return self.file_string

    def _read_file(self):
        handle = open(self.file, 'r')
        var = handle.readlines()
        self.file_string = ''.join(var)
        handle.close()     

    def make_chromosome(self):
        definition = re.search('DEFINITION\s*(.*),?\schromosome\s(\d*|\w{1,2})', self.file_string)
        organism = definition.group(1)
        chromosome_id = definition.group(2)

        seq = re.search('ORIGIN(.*)//', self.file_string, re.DOTALL).group(1)
        seq = re.sub('\n|\s|\d', '', seq)

        self.chromosome = Chromosome(seq, chromosome_id, organism)

        return self.chromosome

    def make_genes(self):

        cds_info = re.findall('CDS(.+?)/translation', self.file_string, re.DOTALL)
        gene_list = []

        for cur_cds in cds_info:

            if re.match('.*complement', cur_cds):
                strand = '+'
            else:
                strand = '-'
            exon_regions = re.findall('.(\d*)\.\.>?(\d*)', cur_cds, re.DOTALL)

            exon_seqs = dict()
            for i, exon in enumerate(exon_regions):
                gen_seq = self.chromosome.seq[int(exon[0]):int(exon[1])]
                exon_seqs.update({exon[0]+'..'+exon[1]: gen_seq})



            gene_id = re.search('/db_xref="GeneID:(\d*)', cur_cds).group(1)

            protein_id = re.search('/protein_id="(.*)"', cur_cds).group(1)
            protein_name = re.search('/product=(".+?")', cur_cds, re.DOTALL).group(1).split(',')[0]
            protein_name = re.sub(' +', ' ', protein_name)
            protein_name = re.sub('\n|"', '', protein_name)

            gene_list.append(Gene(gene_id, strand, exon_regions, exon_seqs, protein_name, protein_id,
                                  self.chromosome))
        self.genes = gene_list

        return self.genes


class Chromosome:

    def __init__(self, seq, chromosome_id, organism):
        self.chromosome_id = chromosome_id
        self.seq = seq
        self.organism = organism
        self.genes = None


class Gene:

    def __init__(self, gene_id, strand, exon_regions, exon_seqs, protein, protein_id, chromosome):
        self.gene_id = gene_id
        self.chromosome_id = chromosome.chromosome_id
        self.organism = chromosome.organism
        self.strand = strand
        self.exon_regions = exon_regions
        self.exon_seqs = exon_seqs
        self.protein = protein
        self.protein_id = protein_id


class FastaHandler:

    def __init__(self):
        pass

    def write_genes(self, genes):
        filename = 'chromosome' + genes[0].chromosome_id + '_' + genes[0].organism + '_genes'

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection!

        else:
            file = open(filename, 'w')
            # TODO make it so that the seqeunce is written to the file
            for gene in genes:
                fasta_id = '>gene_' + str(gene.gene_id) + '|' + str(gene.strand) + '|' + str(gene.protein) + '\n'
                file.write(fasta_id)

                gen_seq = ''.join([value for key, value in gene.exon_seqs.items()]) + '\n\n'

                seq_to_write = []
                for i in range(0, len(gen_seq), 75):
                    seq_to_write.append(gen_seq[i:i+75])
                file.write('\n'.join(seq_to_write))

            file.close()

    def write_chromosome(self, chromosome):
        filename = 'chromosome' + str(chromosome.chromosome_id) + '_' + str(chromosome.organism)

        if os.path.exists(filename):
            print('file exists already')
            # TODO build proper naming and path selection!

        else:
            file = open(filename, 'w')
            fasta_id = '>chromosome_' + str(chromosome.chromosome_id) + '|' + str(chromosome.organism) + '\n'
            file.write(fasta_id)

            seq_to_write = []
            for i in range(0, len(chromosome.seq), 75):
                seq_to_write.append(chromosome.seq[i:i+75])

            file.write('\n'.join(seq_to_write))
            file.close()


def main():
    genbank = GenBank('chromosome_1.gb')
    chromosome1 = genbank.make_chromosome()
    chromosome1.genes = genbank.make_genes()

    fasta_handler = FastaHandler()
    fasta_handler.write_chromosome(chromosome1)
    fasta_handler.write_genes(chromosome1.genes)


if __name__ == '__main__':
    main()
