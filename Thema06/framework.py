#!/usr/bin/env python3
import cgitb
cgitb.enable()
"""
The "framework" module (for lack of a better name) containt everything to setup a basic website.
This functionalaty is located in the MainPage class. The Table class containts everythng to turn
a list of dictionarys into a html table. Finaly the DialogBox class is called when someone
wants to create a "dialog box" or popup screen. In the case of the databases_assingment_one module
a dialog box is called when one of the student names is clicked.
"""


class MainPage():
    """
    This class contains all of the html code needed to create the basic website.
    This html code is devided into sections:
        - Header
        - Sidebar
        - Content
        - java script
    And 4 static methods for calling the html open and close tags.
    This is not nessacery but it makes the code way more readable in my opinion.
    Organising it this way means that parts of the code can easly be reused.
    Parts of the html code, css and javascript have been "borrowed" from a 'framework'
    called bootstrap. Howerver I have only used the 'pure' html code. The creating of
    the tables etc I did do myself. Bootstrap just helps make everything look better
    and allows you to spend more time coding rather than styling your website.
    """

    def __init__(self):
        self.head = ""
        self.sidebar = ""
        self.body_content = ""
        self.js = ""

    def get_head(self, page_title='Olivier Bakker.nl'):
        """
        This method returns all of the code in the head section
        it has an argument called page_title wich is defaulted to Olivier Bakker.nl.
        This argument is the title of the page.

        :return: a string containing the head section of html code.
        """

        self.head = ('<head>'
                     '<meta charset="utf-8">'
                     '<meta http-equiv="X-UA-Compatible" content="IE=edge">'
                     '<meta name="viewport" content="width=device-width, initial-scale=1">'
                     '<meta name="description" content="">'
                     '<meta name="Olivier Bakker" content="">'
                     '<link rel="icon" href="../../../images/favico.png"/>'
                     '<title>' + page_title + '</title>'
                     '<!-- Bootstrap Core CSS -->'
                     '<link href="../../../Resources/css/bootstrap.min.css" rel="stylesheet">'
                     '<!-- Custom CSS -->'
                     '<link href="../../../Resources/css/simple-sidebar.css" rel="stylesheet">'
                     '<script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>'
                     '<script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>'
                     '</head>')

        return self.head

    def get_sidebar(self):
        """
        :return: a string containing the html code for the sidebar
        """

        self.sidebar = ('<!-- Sidebar -->'
                        '<div id="sidebar-wrapper">'
                        '<ul class="sidebar-nav">'
                        '<li class="sidebar-brand">'
                        '<a href="../../Home/index.py">'
                        'Home'
                        '</a>'
                        '</li>'
                        '<li>'
                        '<a href="databases_assignment_one.py">Databases assingement one</a>'
                        '</li>'
                        '<li><a href="contigs_table.py">Contigs</a></li>'
                        '</ul>'
                        '</div>'
                        '<!-- /#sidebar-wrapper -->')

        return self.sidebar

    def get_body_content(self, content):
        """
        This method gets content as an argument. Content is a string containting
        html code. This can be something like a table or just plain text.

        :return: a string containing all of the body section.
        """

        self.body_content += ('<!-- Page Content -->'
                              '<div id="page-content-wrapper">'
                              '<div class="container-fluid">'
                              '<div class="row">'
                              '<div class="col-lg-12">'
                              '<button type="button" href="#menu-toggle" class="btn btn-default" id="menu-toggle">'
                              '<span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>'
                              '<span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>'
                              '</button>'
                              + content +
                              '</div>'
                              '</div>'
                              '</div>'
                              '<!-- /#page-content-wrapper -->')

        return self.body_content

    def get_java_script(self):
        """
        :return: the javascript bootstrap need to operate. It uses this javascript to
        operate the dialog boxes in the databases_assingment_one module for example.
        """

        self.js = ('<script src="../../../Resources/js/jquery.js"></script>'
                   '<script src="../../../Resources/js/bootstrap.js"></script>'
                   '<!-- Menu Toggle Script -->'
                   '<script>'
                   '    $("#menu-toggle").click(function(e) {'
                   '        e.preventDefault();'
                   '        $("#wrapper").toggleClass("toggled");'
                   '    });'
                   '</script>')

        return self.js

    @staticmethod
    def open_html():
        return '<!DOCTYPE html><html>'

    @staticmethod
    def open_body():
        return '<body>'

    @staticmethod
    def close_html():
        return '</html>'

    @staticmethod
    def close_body():
        return '</body>'


class Table():
    """
    This class contains 2 methods:
        - get_static_table returns a "static" table with no interaction.
        - get_linked_table returns a table in wich a collum is linked to an DialogBox object
    These 2 functions are very similar. I tried to create a "static" table by using the
    get_linked_table without any arguments and this worked but it also introduced a bug
    where it would print semi random \n\n\n\n and })' characters. So I decided after tying and
    failing to fix this bug just to make the get_static_table method.
    """

    def __init__(self):
        self.table_html = ""

    def get_static_table(self, data_list):
        """
        Creates a basic table with no interaction.
        :param data_list: A list of dicts containing data to be put in an table.
        :return: html code needed for a table to be produced.
        """

        records = ""
        collumn_names = ""

        # Creates the table header.
        # Filters the collumn names so that the collumn names only appear onte time per table.
        collumn_name_set = set([key for record_dict in data_list for key in record_dict.keys()])
        collumn_names += '<tr>'
        for collumn_name in collumn_name_set:
            collumn_names += ('<th>'+str(collumn_name).capitalize()+'</th>')
        collumn_names += '</tr>'

        # Genarates the records to be displayed.
        for record_dict in data_list:

            records += '<tr>'
            for entry in collumn_name_set:
                    records += ('<td>'+str(record_dict[entry])+'</td>')

            records += '</tr>'

        # Genarates the html to print the table.
        self.table_html += ('<table class="table table-bordered">'
                            '<thead>' + collumn_names + '</thead>'
                            + records + '</table>')

        return self.table_html

    def get_linked_table(self, data_list, primary_collumn, url_list, link_collumn='no_link'):
        """
        This function creates a table in wich one collumn is linked to a specifick action.
        In this case this action is calling a dialog box.

        :param data_list: A list of dicts containing records from wich a table must be made
        :param primary_collumn: Gives the programmer the oppertunity to select a unique collom. This is neccasery
        :param link_collumn: Gives the programmer the oppertunity to select the collumn in wich the
                            links will be genarated. If this is left default the primary_collumn wil be this collumn.
        :return: It returns a tuple containing the HTML code to create the table and an list containing
                the DialogBox objects.
        """

        records = ""
        collumn_names = ""
        i = 0
        # Creates the table header.
        # Filters the collumn names so that the collumn names only appear onte time per table.
        collumn_name_set = set([key for record_dict in data_list for key in record_dict.keys()])
        collumn_names += '<tr>'
        for collumn_name in collumn_name_set:
            collumn_names += ('<th>'+str(collumn_name).capitalize()+'</th>')
        collumn_names += '</tr>'

        for record_dict in data_list:

            # Creates the records to be displayed.
            records += '<tr>'

            # If no link collumn is specified the collumn containing the links is eqeual to the primary collumn.
            if link_collumn == 'no_link':
                link_collumn = primary_collumn

            for entry in collumn_name_set:

                # If the current entry in the dict is equal to the link collumn a 'link' is generated.
                if entry == link_collumn:
                    # Add the link between the dialog box object and the student name.
                    records += ('<td><a  href="{0}">'.format(url_list[i])
                                + str(record_dict[link_collumn]).capitalize()+'</a></td>')
                    i += 1
                else:
                    # If the collumn isn't linked the record is added 'normaly'
                    records += ('<td>'+str(record_dict[entry])+'</td>')
            # Close the record entry
            records += '</tr>'

        # Genarates the html to print the table.
        self.table_html += ('<table class="table table-bordered">'
                            '<thead>' + collumn_names + '</thead>'
                            + records + '</table>')

        return self.table_html


class DialogBox():
    """
    This class contains the framework for the dialog box objects.
    """

    def __init__(self, dialog_title, content, dialog_name='curModal'):
        self.dialog_box_html = ""
        self.dialog_title = dialog_title
        self.content = content
        self.dialog_name = dialog_name

    def create_dialog_box(self):
        """
        This mehtod creates the html code for the dialog boxes. It gets a name a tile and some content
        in the constructor method.
        :return: A string of html code needed to create a dialog box object.
        """

        if len(self.content) < 1:
            self.content = 'No data availible.'

        self.dialog_box_html += ('<div class="modal fade" id ='+str(self.dialog_name)+' role = "dialog">'
                                 '<div class="modal-dialog">'
                                 '<div class="modal-content">'
                                 '<div class="modal-header">'
                                 '<h4 class="modal-title">'+str(self.dialog_title)+'</h4>'
                                 '</div><div class="modal-body"><p>'+str(self.content)+'</p>'
                                 '</div>'
                                 '<div class="modal-footer">'
                                 '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
                                 '</div>'
                                 '</div><!-- /.modal-content -->'
                                 '</div><!-- /.modal-dialog -->'
                                 '</div><!-- /.modal -->')
        return self.dialog_box_html

    def alert_box(self):


        self.dialog_box_html += ('<div class="modal fade" id ='+str(self.dialog_name)+' role = "dialog">'
                                 '<div class="modal-dialog">'
                                 '<div class="modal-content">'
                                 '<div class="modal-body"><p>'
                                 '<div class="alert alert-danger">'
                                 + '<h4>' + str(self.dialog_title)
                                 + str(self.content)  +
                                 '<button type="button" class="close" data-dismiss="modal">&times;</button>' + '</h4>'
                                 '</div>'
                                 '</p></div>'
                                 '</div><!-- /.modal-content -->'
                                 '</div><!-- /.modal-dialog -->'
                                 '</div><!-- /.modal -->')

        return self.dialog_box_html



