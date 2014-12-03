#!/usr/bin/python3
import genbank_parser
import website
import cgi
import cgitb
import tarfile


def main():
    cgitb.enable()

    # Get url parameters
    form = cgi.FieldStorage()

    # Create Website object for required HTML
    html = website.Website()

    # Set content type
    print("Content-Type: text/html")
    print()

    print(html.get_header("GenBank parser"))

    if 'file' in form.keys():
        filefield = form['file']

        if not isinstance(filefield, list):
            filefield = [filefield]

        file_list = list()

        for fileitem in filefield:
            file = fileitem.file.read()
            file = file.decode("utf-8")

            genbank = genbank_parser.GenBank(file)
            chromosome = genbank.make_chromosome()
            chromosome.genes = genbank.make_genes()

            output_file = genbank_parser.FastaWriter.write_chromosome(chromosome, "file/")

            file_list.append(output_file)

        output_filename = 'file/output.tar.gz'

        tar = tarfile.open(output_filename, "w:gz")
        for x in file_list:
            tar.add(x)
        tar.close()

        print('<script>')
        print('window.open("' + output_filename + '");')
        print('</script>')

    print('<form enctype="multipart/form-data" action=web_interface.py method="post">')
    print('<p>File: <input type="file" name="file" multiple=""></p>')
    print('<p><input type="submit" value="Upload"></p>')
    print('</form>')

    # test
    # End with footer
    print(html.get_footer())

if __name__ == '__main__':
    main()