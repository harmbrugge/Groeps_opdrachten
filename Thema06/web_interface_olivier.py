#!/usr/bin/python3
import genbank_parser
import framework
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
            gene = genbank.make_genes()

            chromosome_file = genbank_parser.FastaWriter.get_chromosome_string(chromosome)
            gene_file = genbank_parser.FastaWriter.get_gene_string(gene)
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


class Forms:

    @staticmethod
    def parser_form():
        #nr_nuc_mono_repeat=3, nr_nuc_di_repeat=2, probe_length=20, coverage=10

        string = ('<form class="form" role="form" enctype="multipart/form-data" '
                  'action=web_interface.py method="post">'
                '<div class="form-group">'
                  '<label for="file">File: </label>'
                  '<input id="file" type="file" name="file" multiple="">'
                  '</div>'
                '<div class="form-group">'
                  '<div class="checkbox">'
                  '<label><input type="checkbox" name="check_box">Make probes </label>'
                  '</div></div>'
                '<div class="form-group">'
                  '<label for=mono_rep>Max number mono repeats:</label>'
                  '<div class="col-xs-2">'
                  '<select class="form-control" name="mono_rep">'
                  '<option>1</option>'
                  '<option>2</option>'
                  '<option>3</option>'
                  '<option>4</option>'
                  '</select></div></div>'
                '<div class="form-group">'
                  '<label for=di_rep>Max number di repeats:</label>'
                  '<div class="col-xs-2">'
                  '<select class="form-control" name="di_rep">'
                  '<option>1</option>'
                  '<option>2</option>'
                  '<option>3</option>'
                  '</select></div></div>'
                '<div class="form-group">'
                  '<label for=probe_len>Probe lenght:</label>'
                  '<div class="col-xs-2">'
                  '<select class="form-control" name="probe_len">'
                  '<option>20</option>'
                  '<option>21</option>'
                  '<option>22</option>'
                  '<option>23</option>'
                  '<option>24</option>'
                  '<option>25</option>'
                  '</select></div></div>'
                '<div class="form-group">'
                  '<label for=probe_len>Nucleotide frame skip:</label>'
                  '<div class="col-xs-2">'
                  '<select class="form-control" name="covarage">'
                  '<option>10</option>'
                  '<option>15</option>'
                  '<option>20</option>'
                  '</select></div></div>'
                  '</div>'
                  '<button class="btn btn-default" type="submit" value="Upload">Submit</button>'
                  '</form>')
        return string


def main():
    #cgitb.enable()

    # Get url parameters
    form = cgi.FieldStorage()

    # Create Website object for required HTML
    html = framework.MainPage()

    # Set content type
    print("Content-Type: text/html")
    print()

    # print(html.get_java_script())
    print(html.open_html())
    print(html.open_body())
    print(html.get_head("GenBank parser"))

    print(html.open_wrapper())  # Open the page wrapper
    print(html.get_sidebar())
    print(html.get_body_content('<h1>Genbank Parser</h1>'
                                'This is the genbank parser for the project.'))

    # extra content
    print(Forms().parser_form())

    if 'file' in form.keys():
        filefield = form['file']
        TarFile.get_tarfile(filefield)

    if 'check_box' in form.keys() and form.getvalue('check_box'):

        print('mono_rep: ', form.getvalue('mono_rep'))
        print('di_rep: ', form.getvalue('di_rep'))
        print('probe_len: ', form.getvalue('probe_len'))
        print('nuc frame skip:', form.getvalue('covarage'))

    print(html.close_body_content())  # close the main body section
    print(html.close_wrapper())  # close the wrapper section

    print(html.get_java_script())
    print(html.close_body())
    print(html.close_html())

if __name__ == '__main__':
    main()