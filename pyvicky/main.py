# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from pyvicky.argparser import Argparser
from pyvicky.window import Window
import logging
from pyvicky.logger import Logger


def main():
    logger = Logger('console.log', silent=False)
    app = QApplication(sys.argv)
    window = Window(250, 150, 'file')
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
