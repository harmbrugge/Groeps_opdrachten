#!/usr/bin/env python3


class ParseException(Exception):

    @staticmethod
    def raise_modal(message):
        print('<script type="text/javascript">')
        print("bootbox.alert('<p class=\"lead text-center\">Error ParseException:</p>" + message + "')")
        print('</script>')


