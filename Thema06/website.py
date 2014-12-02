#!/usr/bin/python3


class Website:
    """
    Class with building blocks for a website.
    HTML depends on Bootstrap 3 and custom css,
    installed in ../resources/
    """
    def __init__(self):
        self.header = None
        self.footer = None
        self.table = None

    def get_header(self, title):
        """
        Function to get HTML for header of web-site
        :param title: The title of the web-page
        :return: String with complete html before content
                 (call get_footer for html after content)
        """
        self.header = '<!DOCTYPE html>' \
                      '<html>' \
                      '<head>' \
                      '<title>Harm Brugge - ' + title + '</title>' \
                      '<link rel="icon" href="../resources/img/dna.png"/>' \
                      '<link href="../resources/css/bootstrap.min.css" rel="stylesheet">' \
                      '<link href="../resources/css/main.css" rel="stylesheet">' \
                      '<script type="text/javascript" src="../resources/js/jquery.js"></script>' \
                      '<script src="../resources/js/bootstrap.min.js"></script>' \
                      '<script type="text/javascript" src="../resources/js/bootbox.min.js"></script>' \
                      '</head>' \
                      '<body>' \
                      '<div class="container shadow">' \
                      '<div class="logo">' \
                      '<h1></h1>' \
                      '</div>' \
                      '<br/>' \
                      '<div class="row content">' \
                      '<div class="content-main">' \
                      '<br/>' \
                      '<p class="lead content-title">' + title + '</p>'
        return self.header

    def get_footer(self):
        """
        Function for getting the footer after custom content
        :return: String of HTML
        """
        self.footer = '</div>' \
                      '</div>' \
                      '</div>' \
                      '<div class="footer">' \
                      '<div class="container">' \
                      '<p class="text-muted">Copyright Harm Brugge 2014.</p>' \
                      '</div>' \
                      '</div>' \
                      '</body>' \
                      '</html>'
        return self.footer

    def make_table(self, content):
        """
        Function creates a HTML table out of an iterable
        :param content: Will only work on a list or tuple of Dictionary's for now.
                        Keys must be the same for every item
        :return: String of HTML with table & content
        """
        html = '<table class="table table-condensed">'

        # Check for list or tuple
        if type(content) is list or type(content) is tuple:
            if len(content) > 0:
                # If first item in list is dictionary continue
                if type(content[0]) is dict:
                    # Make table header for every key
                    html += '<thead><tr>'
                    for key in content[0].keys():
                        html += '<th>' + key + '</th>'
                    html += '</tr></thead>'

                    # Make table body
                    html += '<tbody>'
                    for dictonary in content:
                        # New table row for every dict item in list
                        html += '<tr>'
                        # New column for every value in dictionary
                        for value in dictonary.values():
                            html += '<td>' + str(value) + '</td>'
                        html += '</tr>'
                    html += '</tbody>'
            else:
                html += 'No content available'

        html += '</table>'

        self.table = html

        return html