# -*- coding: utf-8 -*-

import sys
# from PyQt5.QtWidgets import QApplication, QWidget
from pyvicky.argparser import Argparser
from pyvicky.window import Window


def main():
    window = Window(250, 150, 'file')
    window.show()
    window.quit()


if __name__ == '__main__':
    main()
