# -*- coding: utf-8 -*-

import argparse
import os
import logging


class Argparser:
    def __init__(self, arguments_string=''):
        self.parser = self.add_parser()
        if arguments_string:
            splitted_arguments_string = arguments_string.split(' ')
            self.args = self.parser.parse_args(splitted_arguments_string)
        else:
            self.args = self.parser.parse_args()

    @staticmethod
    def add_parser():
        parser = argparse.ArgumentParser()

        parser.add_argument('-i', '-interactive', dest='interactive', action='store_true', help='interactive mode')
        parser.add_argument('-f', '-force', dest='force', action='store_true', help='force mode')
        parser.add_argument('-v', '-verbose', dest='verbose', action='store_true', help='verbose mode')
        parser.add_argument('-s', '-silent', dest='silent', action='store_true', help='silent mode, disable logging')

        parser.add_argument('path', nargs='*', help='path of file or directory')
        parser.add_argument('--configs', dest='configs', nargs='*', help='configurations for 1 run')

        return parser
