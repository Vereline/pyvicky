# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

import logging

logger = logging.getLogger('window logger')


class Window(QMainWindow):
    """
    Main window class
    """

    def __init__(self, x, y, filename=''):
        super().__init__()
        self.resize(x, y)
        self.move(300, 300)
        self.setWindowTitle('PyVicky: ' + filename)
        self.setWindowIcon(QIcon('pyvicky/staticfiles/pencil.png'))
        logger.info('Window created')
        self.toolBar = {}
        self.add_menu_bar()
        self.add_tool_bar()
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
        exit_button.triggered.connect(self.close_application)  # replace self.close to normal method(which is need)

        open_button = QAction('Open file', self)
        open_button.setShortcut('Ctrl+O')
        open_button.setStatusTip('Open file')
        open_button.triggered.connect(self.open_file_name_dialog)  # without brackets, else it will execute immediately

        new_button = QAction('New file', self)
        new_button.setShortcut('Ctrl+N')
        new_button.setStatusTip('New file')
        new_button.triggered.connect(self.close)

        save_button = QAction('Save file', self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Save file')
        save_button.triggered.connect(self.save_file_dialog)

        file_menu.addAction(exit_button)
        file_menu.addAction(open_button)
        file_menu.addAction(new_button)
        file_menu.addAction(save_button)

    @staticmethod
    def close_application():
        logger.info('Closing window')
        sys.exit()

    def add_tool_bar(self):
        trash_action = QAction(QIcon('pyvicky/staticfiles/trash.png'), 'Remove item', self)
        trash_action.triggered.connect(self.close_application)

        run_action = QAction(QIcon('pyvicky/staticfiles/next.png'), 'Run interpreter', self)
        run_action.triggered.connect(self.close_application)

        settings_action = QAction(QIcon('pyvicky/staticfiles/settings.png'), 'Interpreter settings', self)
        settings_action.triggered.connect(self.close_application)

        info_action = QAction(QIcon('pyvicky/staticfiles/information.png'), 'Information', self)
        info_action.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(trash_action)
        self.toolBar.addAction(run_action)
        self.toolBar.addAction(settings_action)
        self.toolBar.addAction(info_action)

    def open_file_name_dialog(self):
        """
        open 1 file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;Python Files (*.py)", options=options)
        if file_name:
            logger.debug(file_name)

    def open_file_names_dialog(self):
        """
        open several files
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            logger.debug(files)

    def save_file_dialog(self):
        """
        save 1 file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            logger.debug(file_name)
