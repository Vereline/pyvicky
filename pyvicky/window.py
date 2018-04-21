# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Window:
    def __init__(self, x, y, filename=''):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.resize(x, y)
        self.window.move(300, 300)
        self.window.setWindowTitle('PyVicky: ' + filename)

    def show(self):
        self.window.show()

    def quit(self):
        sys.exit(self.app.exec_())


class MenuBar:
    pass


class ToolBar:
    pass
