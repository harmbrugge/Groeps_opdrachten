#!/usr/bin/env python3


class ParseException(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'ERROR: ParseException: ' + self.message

    def raise_modal(self):
        print('<script type="text/javascript">')
        print("bootbox.alert('<p class=\"lead text-center\">Error ParseException:</p>" + self.message + "')")
        print('</script>')


