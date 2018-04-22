# -*- coding: utf-8 -*-

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget
from pyvicky.argparser import Argparser
from pyvicky.window import Window
import logging
from pyvicky.logger import Logger


def process_args(args, window):
    for file_name in args:
        if os.path.exists(file_name):
            window.open_file(file_name)
            logging.info("Open existing file")
        else:
            window.new_file()
            logging.info("Create file")
        window.set_title(file_name)


def main():
    # TODO: now only possible with 1 file
    logger = Logger('console.log', silent=False)
    argparser = Argparser()
    app = QApplication(sys.argv)
    window = Window(450, 350, '')
    process_args(argparser.out_list, window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
