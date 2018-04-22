# -*- coding: utf-8 -*-
import configparser
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, \
    QTextEdit, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QSyntaxHighlighter, QTextCharFormat
from pyvicky.highlighter import PythonHighlighter
from pyvicky.preferences import PreferencesDlg
from pyvicky.numberbar import QCodeEditor

import traceback
import logging
import re

logger = logging.getLogger('window logger')
ini_pattern = re.compile('(.)*\.ini')


class Window(QMainWindow):
    """
    Main window class
    """

    def __init__(self, x, y, filename='unknown'):
        super().__init__()
        self.resize(x, y)
        self.move(300, 300)

        self.setWindowTitle('PyVicky: ' + filename)
        self.setWindowIcon(QIcon('pyvicky/staticfiles/pencil.png'))

        logger.info('Window created')
        self.toolBar = {}
        self.highlighter = {}
        self.currentFileName = 'Untitled'
        self.currentFilePath = os.getcwd()
        self.firstSave = True

        self.add_menu_bar()
        self.add_tool_bar()

        # self.text = QTextEdit(self)
        self.text = QCodeEditor(self)
        self.setCentralWidget(self.text)

        self.font = QFont()
        self.settings = configparser.ConfigParser()
        self.config = configparser.ConfigParser()

        self.setup_editor()

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
        exit_button.triggered.connect(self.close)  # replace self.close to normal method(which is need)

        open_button = QAction('Open file', self)
        open_button.setShortcut('Ctrl+O')
        open_button.setStatusTip('Open file')
        open_button.triggered.connect(self.open_file)  # without brackets, else it will execute immediately

        new_button = QAction('New file', self)
        new_button.setShortcut('Ctrl+N')
        new_button.setStatusTip('New file')
        new_button.triggered.connect(self.new_file)

        save_button = QAction('Save file', self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Save file')
        save_button.triggered.connect(self.save_file)

        file_menu.addAction(exit_button)
        file_menu.addAction(open_button)
        file_menu.addAction(new_button)
        file_menu.addAction(save_button)

        copy_text = QAction('Copy', self)
        paste_text = QAction('Paste', self)
        clear_text = QAction('Clear', self)

        copy_text.setShortcut('Ctrl+C')
        copy_text.triggered.connect(self.copy_func)

        paste_text.setShortcut('Ctrl+V')
        paste_text.triggered.connect(self.paste_func)

        # Ctrl+A works by itself
        clear_text.setShortcut('Ctrl+Y')
        clear_text.triggered.connect(self.clear_text)

        edit_menu.addAction(copy_text)
        edit_menu.addAction(paste_text)
        edit_menu.addAction(clear_text)

        edit_highlight = QAction('Preferences', self)
        edit_highlight.setShortcut('Ctrl+P')
        edit_highlight.triggered.connect(self.change_preferences)

        view_menu.addAction(edit_highlight)

        help_edit = QAction('Help', self)
        help_edit.setShortcut('Ctrl+H')
        help_edit.triggered.connect(self.change_preferences)

        help_menu.addAction(help_edit)

        self.setMenuWidget(main_menu)
        self.setMenuBar(main_menu)

    @staticmethod
    def close_application():
        logger.info('Closing window')
        sys.exit()

    def add_tool_bar(self):

        # TODO: create new tab
        new_action = QAction(QIcon('pyvicky/staticfiles/plus.png'), 'New item', self)
        new_action.triggered.connect(self.new_file)

        # TODO: clean this file and delete, if exists ???
        trash_action = QAction(QIcon('pyvicky/staticfiles/trash.png'), 'Remove item', self)
        trash_action.triggered.connect(self.clear_text)

        run_action = QAction(QIcon('pyvicky/staticfiles/next.png'), 'Run interpreter', self)
        run_action.triggered.connect(self.close_application)

        settings_action = QAction(QIcon('pyvicky/staticfiles/settings.png'), 'Interpreter settings', self)
        settings_action.triggered.connect(self.close_application)

        # TODO: implement info in file and open in dialog window
        info_action = QAction(QIcon('pyvicky/staticfiles/information.png'), 'Information', self)
        info_action.triggered.connect(self.about)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(new_action)
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
                                                   "All Files (*);;Python Files (*.py);;INI files (*.ini)",
                                                   options=options)
        if file_name:
            logger.debug(file_name)
            # self.open_file(file_name)
            return file_name

        return None

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
            logger.info('Files opened')
            return files

    def open_file(self, filename=None):
        try:
            if not filename:
                filename = self.open_file_name_dialog()

            if filename:
                self.text.setPlainText(open(filename).read())
                logger.info('File opened')
                self.set_title(filename)
        except IOError as io_e:
            logger.error(io_e)
            sys.exit(1)

        except Exception as e:
            logger.error(e)
            sys.exit(1)

    def open_files(self):
        # TODO: not implemented, implement, when tabs will be created
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", '', "All Files (*)")
        try:
            self.text.setPlainText(open(filename).read())

        except IOError as io_e:
            logger.error(io_e)
            sys.exit(1)

        except Exception as e:
            logger.error(e)
            sys.exit(1)

    def save_file_dialog(self):
        """
        save 1 file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
                                                   options=options)
        if file_name:
            logger.debug(file_name)
            # self.save_file(file_name)
            return file_name

        return None

    def save_file(self):
        try:
            file_name = self.save_file_dialog()
            with open(file_name, "w") as CurrentFile:
                CurrentFile.write(self.text.toPlainText())
            CurrentFile.close()
            self.set_title(file_name)
            logger.info('File saved')

        except IOError as io_e:
            logger.error(io_e)
            sys.exit(1)

        except Exception as e:
            logger.error(e)
            sys.exit(1)

    def copy_func(self):
        self.text.copy()

    def paste_func(self):
        self.text.paste()

    def track_unsaved_file(self):
        # TODO BUG:ask to save even if file is saved(when new file is created and saved)??
        destroy = self.text.document().isModified()
        # print(destroy)

        if not destroy:
            return False
        else:
            detour = QMessageBox.question(self,
                                          "Hold your horses.",
                                          "File has unsaved changes. Save now?",
                                          QMessageBox.Yes | QMessageBox.No |
                                          QMessageBox.Cancel)
            if detour == QMessageBox.Cancel:
                return True
            elif detour == QMessageBox.No:
                return False
            elif detour == QMessageBox.Yes:
                return self.save_file()

        return True

    def closeEvent(self, event):
        """
        not a method, but event from QMainWindow
        so, its name should be camel - cased
        :param event:
        :return:
        """
        if self.track_unsaved_file():
            event.ignore()
        else:
            self.close_application()

    def new_file(self):
        # TODO: implement tabs instead of clearing
        if not self.track_unsaved_file():
            self.clear_text()
            logger.info('File created')

    def clear_text(self):
        self.text.clear()

    def set_title(self, file_path):
        file_path = file_path.split('/')[-1]
        self.setWindowTitle('PyVicky: ' + file_path)

    def setup_editor(self):
        # default values
        self.load_config()

        # TODO: set font config with editor (or separated file)
        self.font.setFamily(self.settings.get('Editor', 'Font', fallback='Courier'))
        self.font.setFixedPitch(self.settings.getboolean('Editor', 'FixedPitch', fallback=True))
        self.font.setPointSize(self.settings.getint('Editor', 'FontSize', fallback=11))
        self.font.setWordSpacing(self.settings.getfloat('Editor', 'WordSpacing', fallback=1.0))
        # TODO: set font config with editor (or separated file)

        self.highlighter = PythonHighlighter(self.text.document())

        # set background and main colors
        self.text.setPalette(self.highlighter.get_palette())
        self.text.setTabStopWidth(40)
        self.text.setFont(self.font)

    def load_config(self):
        self.settings.read('pyvicky/configs/settings.ini')
        self.config.read(self.settings['Editor']['theme'])

    def change_preferences(self):
        try:
            # Create the Preferences dialog
            dlg = PreferencesDlg(self)
            dlg.show()
            dlg.accepted.connect(self.update_ui)
        except Exception as e:  # If failed to open Preferences dialog, just open the settings file
            self.currentFilePath = os.path.join(os.getcwd(), 'pyvicky/configs/settings.ini')
            self.currentFileName = 'settings.ini'
            self.firstSave = False

            with open(self.currentFilePath, 'r') as f:
                self.text.clear()
                self.text.setPlainText(f.read())

            logging.error(e)
            traceback.print_exc()

    def update_ui(self):
        # Reload the config
        self.load_config()

        if self.settings.getboolean('Editor', 'ShowLineNumbers', fallback=False):
            self.numberBar.show()
        else:
            self.numberBar.hide()

        self.setup_editor()
        self.text.update()
        self.update()
        logging.info("Updated preferences")

    def about(self):
        QMessageBox.about(self, "About Syntax Highlighter",
                          "<p>The <b>Syntax Highlighter</b> example shows how to " 
                          "perform simple syntax highlighting by subclassing the " 
                          "QSyntaxHighlighter class and describing highlighting " 
                          "rules using regular expressions.</p>")


class DirectoriesTreeView:
    pass


class TabView:
    pass
