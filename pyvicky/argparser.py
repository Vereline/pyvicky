# -*- coding: utf-8 -*-

import argparse
import os
import logging
import sys


class Argparser:
    def __init__(self):
        self.parser = self.add_parser()
        logging.info('Parser created')
        self.defined_command_line = sys.argv[1:]
        self.out_list = self.create_out_list(self.defined_command_line)

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

    @staticmethod
    def define_path(filename):
        if os.path.exists(filename):
            return os.path.abspath(os.path.expanduser(filename))  # filename
        if filename.find('/') == -1:
            path = os.path.abspath(filename)
            # path = os.path.abspath(os.getcwd()+'/()'.format(filename))
        else:
            path = os.path.abspath(os.path.expanduser(filename))
        return path

    def create_out_list(self, args):
        out_list = list(map(self.define_path, args))
        return out_list
