# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow
from PyQt5.QtGui import QIcon

import logging

logger = logging.getLogger('window logger')


class Window(QMainWindow):
    def __init__(self, x, y, filename=''):
        super().__init__()
        self.resize(x, y)
        self.move(300, 300)
        self.setWindowTitle('PyVicky: ' + filename)
        self.setWindowIcon(QIcon('pyvicky/staticfiles/pencil.png'))
        logger.info('Window created')
        self.add_menu_bar()
        self.show()

    def add_menu_bar(self):
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        edit_menu = main_menu.addMenu('Edit')
        view_menu = main_menu.addMenu('View')
        search_menu = main_menu.addMenu('Search')
        tools_menu = main_menu.addMenu('Tools')
        help_menu = main_menu.addMenu('Help')

        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.setStatusTip('Exit application')
        exit_button.triggered.connect(self.close)

        open_button = QAction('Open file', self)
        open_button.setShortcut('Ctrl+O')
        open_button.setStatusTip('Open file')
        open_button.triggered.connect(self.close)

        new_button = QAction('New file', self)
        new_button.setShortcut('Ctrl+N')
        new_button.setStatusTip('New file')
        new_button.triggered.connect(self.close)

        save_button = QAction('Save file', self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Save file')
        save_button.triggered.connect(self.close)

        file_menu.addAction(exit_button)
        file_menu.addAction(open_button)
        file_menu.addAction(new_button)
        file_menu.addAction(save_button)

    def add_tool_bar(self):
        pass
