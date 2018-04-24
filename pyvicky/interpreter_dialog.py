from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QCheckBox, \
                        QComboBox, QLabel, QGroupBox, QColorDialog, QDialog,  QDoubleSpinBox, QLabel, QFileDialog
from PyQt5.QtGui import QColor
import configparser
import os
import sys
import platform
import logging


class InterpreterDlg(QDialog):
    def __init__(self, parent=None):
        super(InterpreterDlg, self).__init__(parent)
        self.resize(450, 200)
        self.config = None
        self.settings = None
        self.path = None
        self.file = None
        self.keys = None
        self.load_config()

        self.setWindowTitle('InterpreterDlg')
        self.initUi()
        logging.info('open interpreter dialog')
        self.show()

    def initUi(self):
        interp_list = self.search_available_interpreter()
        self.layout = QGridLayout()
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.apply_new_interp)

        self.browse_file_button = QPushButton("Browse", self)
        self.browse_file_button.clicked.connect(self.apply_new_filepath)

        self.interpreter_edit = QLineEdit(self)
        self.file_path_edit = QLineEdit(self)
        self.keys_edit = QLineEdit(self)

        self.interpreter_label = QLabel('Interpreter', self)
        self.file_path_label = QLabel('File path', self)
        self.keys_label = QLabel('Keys', self)

        self.ok = QPushButton('Ok', self)
        self.ok.clicked.connect(self.accept)
        self.cancel = QPushButton('Cancel', self)
        self.cancel.clicked.connect(self.decline)

        self.layout.addWidget(self.interpreter_label, 0, 1)
        self.layout.addWidget(self.interpreter_edit, 0, 2)
        self.layout.addWidget(self.browse_button, 0, 3)
        self.layout.addWidget(self.file_path_label, 1, 1)
        self.layout.addWidget(self.file_path_edit, 1, 2)
        self.layout.addWidget(self.browse_file_button, 1, 3)
        self.layout.addWidget(self.keys_label, 2, 1)
        self.layout.addWidget(self.keys_edit, 2, 2)
        self.layout.addWidget(self.ok, 3, 1)
        self.layout.addWidget(self.cancel, 3, 2)

        self.setLayout(self.layout)

        self.interpreter_edit.setText(self.path)
        self.file_path_edit.setText(self.file)
        self.keys_edit.setText(self.keys)

    def apply_new_interp(self):
        interp = self.open_file_name_dialog()
        self.interpreter_edit.setText(interp)

    def apply_new_filepath(self):
        path = self.open_file_name_dialog()
        self.file_path_edit.setText(path)

    def load_config(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('pyvicky/configs/interpreter_settings.ini')
        try:
            self.path = self.settings['Interpreter']['path']
            self.file = self.settings['Interpreter']['file']
            self.keys = self.settings['Interpreter']['keys']
        except Exception as e:
            logging.error(e)
            self.config.read('pyvicky/configs/settings.ini')  # Use the default color theme
            self.path = self.config['Interpreter']['path']
            self.file = self.config['Interpreter']['file']
            self.keys = self.config['Interpreter']['keys']

    def change_config(self):
        self.settings['Interpreter']['path'] = self.interpreter_edit.text()
        self.settings['Interpreter']['file'] = self.file_path_edit.text()
        self.settings['Interpreter']['keys'] = self.keys_edit.text()
        # save the config to file
        with open('pyvicky/configs/interpreter_settings.ini', 'w') as f:
            self.settings.write(f)
            logging.info('Settings saved')

    @staticmethod
    def search_available_interpreter():
        # current_platform = platform.platform()
        system = platform.system()
        if system == 'Linux':
            try:
                return str(os.popen('whereis python').read()).split(' ')
            except Exception as e:
                logging.error(e)
        elif system == 'Windows':
            return [sys.executable]
        else:
            logging.error('system is not supported')
            return None

    def open_file_name_dialog(self):
        """
        open 1 file
        :return:
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Get interpreter", "",
                                                   "All Files (*)",
                                                   options=options)
        if file_name:
            logging.debug(file_name)
            return file_name

    def accept(self):
        self.change_config()
        self.destroy()

    def decline(self):
        self.reject()
        self.destroy()
