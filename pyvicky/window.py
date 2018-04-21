# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QMainWindow, QInputDialog, QLineEdit, QFileDialog, \
    QTextEdit, QMessageBox
from PyQt5.QtGui import QIcon

import logging

logger = logging.getLogger('window logger')


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

        self.add_menu_bar()
        self.add_tool_bar()

        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)

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
        new_button.triggered.connect(self.new_file)

        save_button = QAction('Save file', self)
        save_button.setShortcut('Ctrl+S')
        save_button.setStatusTip('Save file')
        save_button.triggered.connect(self.save_file_dialog)

        file_menu.addAction(exit_button)
        file_menu.addAction(open_button)
        file_menu.addAction(new_button)
        file_menu.addAction(save_button)

        copy_text = QAction('Copy', self)
        paste_text = QAction('Paste', self)

        copy_text.setShortcut('Ctrl+C')
        copy_text.triggered.connect(self.copy_func)

        paste_text.setShortcut('Ctrl+V')
        paste_text.triggered.connect(self.paste_func)

        edit_menu.addAction(copy_text)
        edit_menu.addAction(paste_text)

        self.setMenuWidget(main_menu)
        self.setMenuBar(main_menu)

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
            self.open_file(file_name)
            logger.info('File opened')

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


    def open_file(self, filename):
        try:
            self.text.setText(open(filename).read())

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
            self.text.setText(open(filename).read())
        except:
            True

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
            self.save_file(file_name)
            logger.info('File saved')

    def save_file(self, file_name):
        try:
            with open(file_name, "w") as CurrentFile:
                CurrentFile.write(self.text.toPlainText())
            CurrentFile.close()

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
                return self.save_file_dialog()

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
            self.text.clear()
            logger.info('File created')


class DirectoriesTreeView:
    pass
