#!/usr/bin/python3
import genbank_parser
import website
import cgi
import cgitb
import tarfile
import io
import datetime
import exceptions


class TarFile:

    @staticmethod
    def get_tarfile(filefield):
        if not isinstance(filefield, list):
            if not filefield.filename:
                raise exceptions.ParseException("No file uploaded")
            filefield = [filefield]

        file_list = list()

        for fileitem in filefield:
            file = fileitem.file.read()
            file = file.decode("utf-8")

            genbank = genbank_parser.GenBank(content=file, filename=fileitem.filename)
            chromosome = genbank.make_chromosome()
            chromosome.genes = genbank.make_genes()

            chromosome_file = genbank_parser.FastaWriter.get_chromosome_string(chromosome)
            gene_file = genbank_parser.FastaWriter.get_gene_string(chromosome.genes)
            file_list.append(chromosome_file)
            file_list.append(gene_file)

        output_filename = 'file/' + str(datetime.datetime.now()) + '_parsed-fasta-files.tar.gz'

        tar = tarfile.open(output_filename, "w:gz")
        for x in file_list:
            tarinfo = tarfile.TarInfo(x[1])
            tarinfo.size = len(x[0])
            tar.addfile(tarinfo, io.BytesIO(x[0].encode('utf8')))
        tar.close()

        print('<script>window.open("' + output_filename + '");</script>')


def main():
    # cgitb.enable()

    # Get url parameters
    form = cgi.FieldStorage()

    # Create Website object for required HTML
    html = website.Website()

    # Set content type
    print("Content-Type: text/html")
    print()

    print(html.get_header("GenBank parser"))

    print('<form role="form" enctype="multipart/form-data" action=web_interface.py method="post">')
    print('<div class="form-group"><label for="file">File: </label>'
          '<input id="file" type="file" name="file" multiple=""></div>')
    print('<button class="btn btn-default" type="submit" value="Upload">Submit</button>')
    print('</form>')

    if 'file' in form.keys():
        filefield = form['file']
        TarFile.get_tarfile(filefield)

    # End with footer
    print(html.get_footer())

if __name__ == '__main__':
    main()