#!/usr/bin/python3
import genbank_parser
import website
import os
import cgi
import cgitb


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

    message = 'Nog niks gedaan'

    if 'file' in form.keys():
        # Test if the file was uploaded
        if form['file'].filename:
            # strip leading path from file name to avoid directory traversal attacks
            fn = os.path.basename(form['file'].filename)

            file = form['file'].file.read()
            file = file.decode("utf-8")

            genbank = genbank_parser.GenBank(file)
            chromosome = genbank.make_chromosome()
            chromosome.genes = genbank.make_genes()

            output_file = genbank_parser.FastaWriter.write_chromosome(chromosome, "file/")

            print('<script>')
            print('window.open("' + output_file + '");')
            print('</script>')

            # file = open('file/' + fn, 'wb')
            # file.write(form['file'].file.read())



        else:
            message = 'Upload error'



    print('<form enctype="multipart/form-data" action=web_interface.py method="post">')
    print('<p>File: <input type="file" name="file"></p>')
    print('<p><input type="submit" value="Upload"></p>')
    print('</form>')

    # test
    print(message)
    # End with footer
    print(html.get_footer())

if __name__ == '__main__':
    main()