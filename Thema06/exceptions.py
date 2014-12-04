#!/usr/bin/env python3


class ParseException(Exception):

    def __init__(self, message):
        self.message = message


    def __str__(self):
        return 'ERROR: ParseException:' + self.message

