# -*- coding: utf-8 -*-
import configparser
import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, \
    QTextEdit, QMessageBox, QVBoxLayout, QTabWidget, QFileSystemModel, QTreeView, QDockWidget
from PyQt5.QtGui import QIcon, QFont, QSyntaxHighlighter, QTextCharFormat
from pyvicky.highlighter import PythonHighlighter
from pyvicky.preferences import PreferencesDlg
from pyvicky.numberbar import QCodeEditor
from pyvicky.find import Find
from pyvicky.interpreter_dialog import InterpreterDlg

import traceback
import subprocess
import logging
import re
import time

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
        self.findDlg = None

        self.add_menu_bar()
        self.add_tool_bar()

        self.docked_items = QDockWidget("Tree", self)
        self.treeWidget = DirectoriesTreeView(self)
        self.treeWidget.tree.clicked.connect(self.open_file_from_tree)
        self.docked_items.setWidget(self.treeWidget)
        self.docked_items.setFloating(False)
        # self.text = QTextEdit(self)
        # self.text = QCodeEditor(self)
        # self.setCentralWidget(self.text)
        self.tabWidget = TabView(self)
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.docked_items)

        # self.tabWidget.add_tab(self, "new")

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

        open_dir_button = QAction('Open directory', self)
        open_dir_button.setShortcut('Ctrl+Shift+O')
        open_dir_button.setStatusTip('Open directory')
        open_dir_button.triggered.connect(self.open_directory)

        file_menu.addAction(exit_button)
        file_menu.addAction(open_button)
        file_menu.addAction(new_button)
        file_menu.addAction(save_button)
        file_menu.addAction(open_dir_button)

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
        help_edit.triggered.connect(self.about)

        help_menu.addAction(help_edit)
        help_menu.addAction("About Qt", QApplication.instance().aboutQt)

        search_edit = QAction('Search', self)
        search_edit.setShortcut('Ctrl+F')
        search_edit.triggered.connect(self.search_config)

        search_menu.addAction(search_edit)

        interp_edit = QAction('Interpreter Settings', self)
        interp_edit.setShortcut('Ctrl+I')
        interp_edit.triggered.connect(self.interp_settings)

        interp_run = QAction('Run Interpreter', self)
        interp_run.setShortcut('F11')
        interp_run.triggered.connect(self.run_interp)

        tools_menu.addAction(interp_edit)
        tools_menu.addAction(interp_run)

        self.setMenuWidget(main_menu)
        self.setMenuBar(main_menu)

    @staticmethod
    def close_application():
        logger.info('Closing window')
        sys.exit()

    def add_tool_bar(self):

        new_action = QAction(QIcon('pyvicky/staticfiles/plus.png'), 'New item', self)
        new_action.triggered.connect(self.new_file)

        trash_action = QAction(QIcon('pyvicky/staticfiles/trash.png'), 'Clean item', self)
        trash_action.triggered.connect(self.clear_text)

        run_action = QAction(QIcon('pyvicky/staticfiles/next.png'), 'Run interpreter', self)
        run_action.triggered.connect(self.run_interp)

        settings_action = QAction(QIcon('pyvicky/staticfiles/settings.png'), 'Interpreter settings', self)
        settings_action.triggered.connect(self.interp_settings)

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

    def open_dir_dialog(self):
        """
        open directory
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dirs = QFileDialog.getExistingDirectory(self, 'Select directory')

        if dirs:
            logger.debug(dirs)
            logger.info('Dir opened')
            return dirs

    def open_directory(self):
        path = self.open_dir_dialog()
        if path:
            # print(path)
            self.treeWidget.initUI(path)
            return path

    def open_file(self, filename=None):
        try:
            if not filename:
                filename = self.open_file_name_dialog()

            if filename and os.path.isfile(filename):
                self.tabWidget.add_tab(self, filename, open(filename).read())
                # self.text.setPlainText(open(filename).read())
                self.update_ui()
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
            self.tabWidget.add_tab(self, filename, open(filename).read())
            # self.text.setPlainText(open(filename).read())

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

    def save_file(self, current=None):
        try:
            file_name = self.save_file_dialog()
            with open(file_name, "w") as CurrentFile:
                if not current:
                    current = self.tabWidget.get_cur_index()
                CurrentFile.write(self.get_editor_by_index(current).toPlainText())
                # CurrentFile.write(self.text.toPlainText())
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
        current = self.tabWidget.get_cur_index()
        self.get_editor_by_index(current).copy()

    def paste_func(self):
        current = self.tabWidget.get_cur_index()
        self.get_editor_by_index(current).paste()

    def get_editor_by_index(self, current):
        return self.tabWidget.get_editor_from_tab(current)

    def track_unsaved_file(self, current=None):
        # destroy = self.text.document().isModified()
        if current is None:
            current = self.tabWidget.get_cur_index()
        destroy = self.get_editor_by_index(current).document().isModified()

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
                return self.save_file(current)

        return True

    def track_unsaved_files(self):
        count = self.tabWidget.get_tabs()
        result = False
        for i in range(count):
            if not result:  # in order to define, is there any file, which is modified and not saved
                result = self.track_unsaved_file(i)

        return result

    def closeEvent(self, event):
        """
        not a method, but event from QMainWindow
        so, its name should be camel - cased
        :param event:
        :return:
        """
        if self.track_unsaved_files():
            event.ignore()
        else:
            self.close_application()

    def new_file(self):
        self.tabWidget.add_tab(self, "new")
        # self.clear_text()
        self.update_ui()
        logger.info('File created')

    def clear_text(self):
        current = self.tabWidget.get_cur_index()
        self.get_editor_by_index(current).clear()

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

        count = self.tabWidget.get_tabs()
        for i in range(count):
            highlighter = self.tabWidget.set_highlighter(i)
            text = self.tabWidget.get_editor_from_tab(i)
            text.setPalette(highlighter.get_palette())
            text.setTabStopWidth(40)
            text.setFont(self.font)

    def load_config(self):
        self.settings.read('pyvicky/configs/settings.ini')
        self.config.read(self.settings['Editor']['theme'])

    def search_config(self):
        find = Find(self)
        find.show()

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
                self.tabWidget.add_tab(self, "INI", f.read())
                # self.text.clear()
                # self.text.setPlainText(f.read())

            logging.error(e)
            traceback.print_exc()

    def interp_settings(self):
        # Create the Interpreter dialog
        try:
            dlg = InterpreterDlg(self)
        except Exception as e:
            logging.error(e)

    def run_interp(self):
        settings = configparser.ConfigParser()
        settings.read('pyvicky/configs/interpreter_settings.ini')
        print(settings.sections())
        settings_arr = settings.sections()[0]
        # settings_arr = settings.options(settings_arr)
        run_script = ' '.join([settings['Interpreter']['path'],
                               settings['Interpreter']['file'],
                               settings['Interpreter']['keys']])
        logging.debug("SETTINGS: " + run_script)
        try:
            process = subprocess.Popen('echo "Start executing program..."', stdout=subprocess.PIPE, shell=True)
            username = process.communicate()[0]
            # print(username)  # prints the username of the account you're logged in as
            start = time.time()
            process = subprocess.call(run_script, shell=True)
            end = time.time()
            elapsed_time = end - start
            logging.info('Task is done in ' + str(elapsed_time))
            print('Task is successfully done in {time} sec'.format(time=str(elapsed_time)))
        except Exception as e:
            logging.error(e)

    def update_ui(self):
        # Reload the config
        self.load_config()

        self.setup_editor()
        # self.text.update()
        self.update()
        logging.info("Updated preferences")

    def about(self):
        QMessageBox.about(self, "About Syntax PyVicky",
                          "<p>The <b>PyVicky Editor</b> is a simple text editor " 
                          "which perform simple syntax highlighting by subclassing the " 
                          "QSyntaxHighlighter class and describing highlighting " 
                          "rules using regular expressions.</p>")

    def close_tab(self, current_index):
        if self.track_unsaved_file(current_index):
            pass
        else:
            self.tabWidget.close_tab(current_index)

    def open_file_from_tree(self, index):
        # TODO: iterate if file is already opned, or not??=)
        path = self.treeWidget.tree_function(index)
        self.open_file(path)


class DirectoriesTreeView(QWidget):

    def __init__(self, parent, _dir=None):
        super(QWidget, self).__init__(parent)
        self.tree = QTreeView()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.tree)
        self.setLayout(windowLayout)
        logging.info('create tree widget')
        self.initUI(_dir)

    def initUI(self, _dir=None):

        if _dir:
            self.model = QFileSystemModel()
            # self.model.setRootPath('')
            self.model.setRootPath(_dir)
            # print(self.model.rootPath())
            # print(self.model.rootDirectory())
            index = self.model.index(self.model.rootPath())

            self.tree.setModel(self.model)
            self.tree.setRootIndex(index)

            self.tree.setAnimated(False)
            self.tree.setIndentation(20)
            self.tree.setSortingEnabled(True)

            # self.tree.resize(640, 480)
            self.tree.hideColumn(3)  # disable file type, file size etc
            self.tree.hideColumn(2)
            self.tree.hideColumn(1)
            # self.tree.clicked.connect(self.tree_function)
            logging.info('update tree')

        self.show()

    def tree_function(self, index):
        # print(item)
        path = self.sender().model().filePath(index)
        logging.info('Tree path is ' + path)
        return path


class TabView(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabWidget = QTabWidget()

        self.tabWidget.setTabsClosable(True)
        # self.tabWidget.tabCloseRequested.connect(self.close_tab)

        # Add tabs to widget
        self.layout.addWidget(self.tabWidget)
        self.setLayout(self.layout)

    def add_tab(self, parent, tab_name, text=''):
        tab = QWidget()
        tab.layout = QVBoxLayout(self)
        text_editor = QCodeEditor(parent)
        text_editor.setPlainText(text)
        tab.layout.addWidget(text_editor)
        tab.setLayout(tab.layout)
        if '/' in tab_name:
            tab_name = tab_name.split('/')[-1]
        self.tabWidget.addTab(tab, tab_name)
        logging.info('Added tab')

    def close_tab(self, currentIndex):
        # TODO: control save operation
        # currentQWidget = self.widget(currentIndex)
        # currentQWidget.deleteLater()
        self.tabWidget.removeTab(currentIndex)
        logging.info('Closed tab')

    def get_cur_index(self):
        return self.tabWidget.currentIndex()

    def get_cur_text(self):
        index = self.get_cur_index()
        text = self.tabWidget.widget(index).text_editor.toPlainText()
        return text

    def get_editor_from_tab(self, index):
        tab = self.tabWidget.widget(index)
        count = tab.layout.count()
        try:
            for i in range(count):
                if type(tab.layout.itemAt(i).widget()) is QCodeEditor:
                    return tab.layout.itemAt(i).widget()
        except Exception as e:
            logging.error(e)

    def set_highlighter(self, index):
        editor = self.get_editor_from_tab(index)
        self.tabWidget.widget(index).highlighter = PythonHighlighter(editor.document())
        return self.tabWidget.widget(index).highlighter

    def get_tabs(self):
        return self.tabWidget.count()
