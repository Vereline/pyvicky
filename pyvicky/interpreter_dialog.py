from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QCheckBox, \
                        QComboBox, QLabel, QGroupBox, QColorDialog, QDialog,  QDoubleSpinBox, QLabel
from PyQt5.QtGui import QColor
import configparser
import os
import logging


class InterpreterDlg(QDialog):
    def __init__(self, parent=None):
        super(InterpreterDlg, self).__init__(parent)
        self.config = None
        self.settings = None

        self.load_config()

        self.setWindowTitle('InterpreterDlg')
        self.show()

    def load_config(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('pyvicky/configs/interpreter_settings.ini')
        try:
            self.config.read(self.theme)
            self.settings['Editor']['theme'] = self.theme
        except Exception as e:
            logging.error(e)
            self.config.read('pyvicky/configs/themes/default.ini')  # Use the default color theme
            self.settings['Editor']['theme'] = self.theme

    def change_config(self):
        pass

    def search_available_interpreter(self):
        pass