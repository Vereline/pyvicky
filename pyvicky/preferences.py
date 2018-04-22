# preferences dialog
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QLineEdit, QHBoxLayout, QPushButton, QSpinBox, QCheckBox, \
                        QComboBox, QLabel, QGroupBox, QColorDialog, QDialog,  QDoubleSpinBox, QLabel
from PyQt5.QtGui import QColor
import configparser
import os
import logging
from . import highlighter as hl


class PreferencesDlg(QDialog):
    def __init__(self, parent=None):
        super(PreferencesDlg, self).__init__(parent)
        self.config = None
        self.settings = None
        self.theme = ''

        self.load_config()

        self.make_widgets()
        self.set_initial_values()
        self.make_connections()
        self.setWindowTitle('Preferences')

        self.show()

    def load_config(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('pyvicky/configs/settings.ini')
        try:
            self.theme = 'pyvicky/configs/themes/' + self.themeBox.currentText() + '.ini'
        except Exception as e:
            logging.error(e)
            self.theme = ''
        if self.theme == '':
            self.theme = self.settings.get('Editor', 'theme', fallback='pyvicky/configs/themes/default.ini')

        self.config = configparser.ConfigParser()
        try:
            self.config.read(self.theme)
            self.settings['Editor']['theme'] = self.theme
        except Exception as e:
            logging.error(e)
            self.config.read('pyvicky/configs/themes/default.ini')  # Use the default color theme
            self.settings['Editor']['theme'] = self.theme

    def make_widgets(self):
        self.mainLayout = QVBoxLayout()

        self.setup_editor_widgets()
        self.setup_color_widgets()
        self.setup_extensions_widgets()

        button_layout = QHBoxLayout()
        self.saveButton = QPushButton('&Save')
        self.cancelButton = QPushButton('Cancel')
        button_layout.addWidget(self.saveButton)
        button_layout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(button_layout)

        self.setLayout(self.mainLayout)

    def make_connections(self):
        # Color Picker buttons
        self.bgButton.clicked.connect(self.select_bg)
        self.fgButton.clicked.connect(self.select_fg)
        self.singleButton.clicked.connect(self.select_single)
        self.multiButton.clicked.connect(self.select_multi)
        self.stringButton.clicked.connect(self.select_string)
        self.keywordButton.clicked.connect(self.select_keyword)
        self.functionButton.clicked.connect(self.select_function)
        self.highlightButton.clicked.connect(self.select_highlight)
        self.highlightedTextButton.clicked.connect(self.select_highlighted_text)

        # Accept/Cancel buttons
        self.saveButton.clicked.connect(self.save)
        self.cancelButton.clicked.connect(self.cancel)

    @staticmethod
    def get_themes():
        """Parse through the theme dir and get the themes names as strings.
        Returns a list (of theme names)."""
        themes = []
        for file in os.listdir('pyvicky/configs/themes/'):
            if file.endswith('.ini'):
                themes.append(file[:-4])
        return themes

    def set_color_values(self):
        # Get the theme
        self.load_config()

        # Set the widget values
        self.bgInput.setText(self.config['Colors']['Background'])
        self.fgInput.setText(self.config['Colors']['Foreground'])
        self.singleInput.setText(self.config['Colors']['SingleLineComment'])
        self.multiInput.setText(self.config['Colors']['MultiLineComment'])
        self.stringInput.setText(self.config['Colors']['String'])
        self.keywordInput.setText(self.config['Colors']['Keyword'])
        self.functionInput.setText(self.config['Colors']['Function'])
        self.highlightInput.setText(self.config['Colors']['Highlight'])
        self.highlightedTextInput.setText(self.config['Colors']['HighlightedText'])

        color_picker = QColor()
        color_picker.setNamedColor('#' + self.config['Colors']['Background'])
        self.bgLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Foreground'])
        self.fgLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['SingleLineComment'])
        self.singleLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['MultiLineComment'])
        self.multiLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['String'])
        self.stringLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Keyword'])
        self.keywordLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Function'])
        self.functionLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Highlight'])
        self.highlightLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['HighlightedText'])
        self.highlightedTextLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_color_values " + color_picker.name())

    def theme_selected(self):
        # Theme has been selected, now update the other theme setting widgets
        # to contain *that* theme's colors
        self.set_color_values()

    @staticmethod
    def get_highlighters():
        """Parse through the highlighter.py file and get the highlighter class names as strings.
        Returns a list (of class names)."""
        highlighters = []
        classes = dir(hl)
        classes.remove('BaseHighlighter')  # Ignore the base class
        for highlighter in classes:
            if highlighter.endswith('Highlighter'):
                highlighters.append(highlighter)
        return highlighters

    def setup_editor_widgets(self):
        # Editor widgets
        self.fontBox = QLineEdit()
        self.fontSize = QSpinBox()
        self.fontSize.setRange(4, 72)
        self.fixedPitchToggle = QCheckBox('Fixed Pitch')
        self.wordSpacing = QDoubleSpinBox()
        self.wordSpacing.setRange(0.5, 5.0)
        self.useSpaces = QCheckBox('Use Spaces')
        self.spacesPerTab = QSpinBox()
        self.spacesPerTab.setRange(1, 8)
        self.showLineNumbers = QCheckBox('Show Line Numbers')
        self.smartIndent = QCheckBox('Smart Indent')
        self.themeBox = QComboBox()
        themes = self.get_themes()
        self.themeBox.addItems(themes)
        self.themeBox.setCurrentIndex(themes.index(self.settings['Editor']['theme'].split('/')[-1][
                                                   :-4]))  # Set the current item to the the current theme (without the path and .ini part)
        self.themeBox.activated.connect(self.theme_selected)

        # Editor Group
        self.editorLayout = QGridLayout()
        self.editorLayout.addWidget(QLabel('Font:'), 0, 0)
        self.editorLayout.addWidget(self.fontBox, 0, 1)
        self.editorLayout.addWidget(QLabel('Font Size:'), 1, 0)
        self.editorLayout.addWidget(self.fontSize, 1, 1)
        self.editorLayout.addWidget(self.fixedPitchToggle, 2, 0, 1, 2)
        self.editorLayout.addWidget(QLabel('Word Spacing:'), 3, 0)
        self.editorLayout.addWidget(self.wordSpacing, 3, 1)
        self.editorLayout.addWidget(self.useSpaces, 4, 0)
        self.editorLayout.addWidget(QLabel('Spaces Per Tab:'), 5, 0)
        self.editorLayout.addWidget(self.spacesPerTab, 5, 1)
        self.editorLayout.addWidget(self.showLineNumbers, 6, 0)
        self.editorLayout.addWidget(self.smartIndent, 7, 0)
        self.editorLayout.addWidget(QLabel('Theme:'), 8, 0)
        self.editorLayout.addWidget(self.themeBox, 8, 1)

        self.editorGroupBox = QGroupBox('Editor')
        self.editorGroupBox.setLayout(self.editorLayout)
        self.mainLayout.addWidget(self.editorGroupBox)

    def setup_color_widgets(self):
        # Color widgets
        self.bgInput = QLineEdit()
        self.bgLabel = QLabel('    ')
        self.bgButton = QPushButton('Choose...')

        self.fgInput = QLineEdit()
        self.fgButton = QPushButton('Choose...')
        self.fgLabel = QLabel('    ')

        self.singleInput = QLineEdit()
        self.singleButton = QPushButton('Choose...')
        self.singleLabel = QLabel('    ')

        self.multiInput = QLineEdit()
        self.multiButton = QPushButton('Choose...')
        self.multiLabel = QLabel('    ')

        self.stringInput = QLineEdit()
        self.stringButton = QPushButton('Choose...')
        self.stringLabel = QLabel('    ')

        self.keywordInput = QLineEdit()
        self.keywordButton = QPushButton('Choose...')
        self.keywordLabel = QLabel('    ')

        self.functionInput = QLineEdit()
        self.functionButton = QPushButton('Choose...')
        self.functionLabel = QLabel('    ')

        self.highlightInput = QLineEdit()
        self.highlightButton = QPushButton('Choose...')
        self.highlightLabel = QLabel('    ')

        self.highlightedTextInput = QLineEdit()
        self.highlightedTextButton = QPushButton('Choose...')
        self.highlightedTextLabel = QLabel('    ')

        # Color layout
        self.colorLayout = QGridLayout()
        self.colorLayout.addWidget(QLabel('Background:'), 0, 0)
        self.colorLayout.addWidget(self.bgInput, 0, 1)
        self.colorLayout.addWidget(self.bgButton, 0, 3)
        self.colorLayout.addWidget(self.bgLabel, 0, 2)
        self.colorLayout.addWidget(QLabel('Foreground:'), 1, 0)
        self.colorLayout.addWidget(self.fgInput, 1, 1)
        self.colorLayout.addWidget(self.fgButton, 1, 3)
        self.colorLayout.addWidget(self.fgLabel, 1, 2)
        self.colorLayout.addWidget(QLabel('Single Line Comment:'), 2, 0)
        self.colorLayout.addWidget(self.singleInput, 2, 1)
        self.colorLayout.addWidget(self.singleButton, 2, 3)
        self.colorLayout.addWidget(self.singleLabel, 2, 2)
        self.colorLayout.addWidget(QLabel('Mult-Line Comment:'), 3, 0)
        self.colorLayout.addWidget(self.multiInput, 3, 1)
        self.colorLayout.addWidget(self.multiButton, 3, 3)
        self.colorLayout.addWidget(self.multiLabel, 3, 2)
        self.colorLayout.addWidget(QLabel('String:'), 4, 0)
        self.colorLayout.addWidget(self.stringInput, 4, 1)
        self.colorLayout.addWidget(self.stringButton, 4, 3)
        self.colorLayout.addWidget(self.stringLabel, 4, 2)
        self.colorLayout.addWidget(QLabel('Keyword:'), 5, 0)
        self.colorLayout.addWidget(self.keywordInput, 5, 1)
        self.colorLayout.addWidget(self.keywordButton, 5, 3)
        self.colorLayout.addWidget(self.keywordLabel, 5, 2)
        self.colorLayout.addWidget(QLabel('Function:'), 6, 0)
        self.colorLayout.addWidget(self.functionInput, 6, 1)
        self.colorLayout.addWidget(self.functionButton, 6, 3)
        self.colorLayout.addWidget(self.functionLabel, 6, 2)
        self.colorLayout.addWidget(QLabel('Highlight:'), 7, 0)
        self.colorLayout.addWidget(self.highlightInput, 7, 1)
        self.colorLayout.addWidget(self.highlightButton, 7, 3)
        self.colorLayout.addWidget(self.highlightLabel, 7, 2)
        self.colorLayout.addWidget(QLabel('Highlighted Text:'), 8, 0)
        self.colorLayout.addWidget(self.highlightedTextInput, 8, 1)
        self.colorLayout.addWidget(self.highlightedTextButton, 8, 3)
        self.colorLayout.addWidget(self.highlightedTextLabel, 8, 2)

        # Color Group
        self.colorGroupBox = QGroupBox('Colors')
        self.colorGroupBox.setLayout(self.colorLayout)
        self.mainLayout.addWidget(self.colorGroupBox)

    def setup_extensions_widgets(self):
        # Extensions Widgets
        highlighters = self.get_highlighters()
        self.highlighter = QComboBox()
        self.highlighter.addItems(highlighters)
        self.highlighter.setCurrentIndex(highlighters.index(self.settings['Extensions'][
                                                                'highlighter']))
        # Set the current item to the the current theme (without the path and .ini part)

        # Extensions Layout
        self.extensionsLayout = QGridLayout()
        self.extensionsLayout.addWidget(QLabel('Highlighter Class:'))
        self.extensionsLayout.addWidget(self.highlighter)

        # Extensions Group
        self.extensionsGroupBox = QGroupBox('Extensions')
        self.extensionsGroupBox.setLayout(self.extensionsLayout)
        self.mainLayout.addWidget(self.extensionsGroupBox)

    def set_initial_values(self):
        self.fontBox.setText(self.settings['Editor']['Font'])
        self.fontSize.setValue(self.settings.getint('Editor', 'FontSize'))
        self.fixedPitchToggle.setChecked(self.settings.getboolean('Editor', 'FixedPitch'))
        self.wordSpacing.setValue(self.settings.getfloat('Editor', 'WordSpacing'))
        self.useSpaces.setChecked(self.settings.getboolean('Editor', 'UseSpaces'))
        self.spacesPerTab.setValue(self.settings.getint('Editor', 'SpacesPerTab'))
        self.showLineNumbers.setChecked(self.settings.getboolean('Editor', 'ShowLineNumbers'))
        self.smartIndent.setChecked(self.settings.getboolean('Editor', 'smartindent'))

        self.bgInput.setText(self.config['Colors']['Background'])
        self.fgInput.setText(self.config['Colors']['Foreground'])
        self.singleInput.setText(self.config['Colors']['SingleLineComment'])
        self.multiInput.setText(self.config['Colors']['MultiLineComment'])
        self.stringInput.setText(self.config['Colors']['String'])
        self.keywordInput.setText(self.config['Colors']['Keyword'])
        self.functionInput.setText(self.config['Colors']['Function'])
        self.highlightInput.setText(self.config['Colors']['Highlight'])
        self.highlightedTextInput.setText(self.config['Colors']['HighlightedText'])

        color_picker = QColor()
        color_picker.setNamedColor('#' + self.config['Colors']['Background'])
        self.bgLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Foreground'])
        self.fgLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['SingleLineComment'])
        self.singleLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['MultiLineComment'])
        self.multiLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['String'])
        self.stringLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Keyword'])
        self.keywordLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Function'])
        self.functionLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['Highlight'])
        self.highlightLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        color_picker.setNamedColor('#' + self.config['Colors']['HighlightedText'])
        self.highlightedTextLabel.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())
        logging.debug("set_initial_values " + color_picker.name())

        highlighters = self.get_highlighters()
        self.highlighter.setCurrentIndex(highlighters.index(self.settings['Extensions'][
                                                                'highlighter']))
        # Set the current item to the the current theme (without the path and .ini part)

    def get_values(self):
        """Reads the values from the preference widgets and
        stores them in the self.settings and self.config ConfigParser object."""
        # Get correct configs/theme
        self.load_config()

        self.settings.set('Editor', 'Font', self.fontBox.text())
        self.settings.set('Editor', 'FontSize', str(self.fontSize.value()))
        temp = 'yes' if self.fixedPitchToggle.isChecked() else 'no'
        self.settings.set('Editor', 'FixedPitch', temp)
        self.settings.set('Editor', 'WordSpacing', str(self.wordSpacing.value()))
        temp = 'yes' if self.useSpaces.isChecked() else 'no'
        self.settings.set('Editor', 'UseSpaces', temp)
        self.settings.set('Editor', 'SpacesPerTab', str(self.spacesPerTab.value()))
        temp = 'yes' if self.showLineNumbers.isChecked() else 'no'
        self.settings.set('Editor', 'ShowLineNumbers', temp)
        temp = 'yes' if self.smartIndent.isChecked() else 'no'
        self.settings.set('Editor', 'smartindent', temp)
        self.settings.set('Editor', 'theme', 'pyvicky/configs/themes/' + self.themeBox.currentText() + '.ini')

        self.config.set('Colors', 'Background', self.bgInput.text())
        self.config.set('Colors', 'Foreground', self.fgInput.text())
        self.config.set('Colors', 'SingleLineComment', self.singleInput.text())
        self.config.set('Colors', 'MultiLineComment', self.multiInput.text())
        self.config.set('Colors', 'String', self.stringInput.text())
        self.config.set('Colors', 'Keyword', self.keywordInput.text())
        self.config.set('Colors', 'Function', self.functionInput.text())
        self.config.set('Colors', 'Highlight', self.highlightInput.text())
        self.config.set('Colors', 'HighlightedText', self.highlightedTextInput.text())

        self.settings.set('Extensions', 'Highlighter', self.highlighter.currentText())

    def make_color_dlg(self, line_edit, color_label):
        color_dlg = QColorDialog(self)
        color_dlg.setCurrentColor(QColor('#' + line_edit.text()))
        color_dlg.show()

        def update():
            color = color_dlg.currentColor()
            rVal, gVal, bVal, aVal = color.getRgb()
            # Pad the hex string, if needed
            color_string = ''
            if rVal < 0x0F:
                color_string += '0'
            color_string += '%x' % rVal
            if gVal < 0x0F:
                color_string += '0'
            color_string += '%x' % gVal
            if bVal < 0x0F:
                color_string += '0'
            color_string += '%x' % bVal
            line_edit.setText(color_string)
            color_picker = QColor()
            color_picker.setNamedColor('#' + color_string)
            logging.debug("make_color_dlg " + color_picker.name())
            color_label.setStyleSheet("QLabel { background-color: %s }" % color_picker.name())

        color_dlg.accepted.connect(update)

    def select_bg(self):
        self.make_color_dlg(self.bgInput, self.bgLabel)

    def select_fg(self):
        self.make_color_dlg(self.fgInput, self.fgLabel)

    def select_single(self):
        self.make_color_dlg(self.singleInput, self.singleLabel)

    def select_multi(self):
        self.make_color_dlg(self.multiInput, self.multiLabel)

    def select_string(self):
        self.make_color_dlg(self.stringInput, self.stringLabel)

    def select_keyword(self):
        self.make_color_dlg(self.keywordInput, self.keywordLabel)

    def select_function(self):
        self.make_color_dlg(self.functionInput, self.functionLabel)

    def select_highlight(self):
        self.make_color_dlg(self.highlightInput, self.highlightLabel)

    def select_highlighted_text(self):
        self.make_color_dlg(self.highlightedTextInput, self.highlightedTextLabel)

    def save(self):
        # Get values into self.config
        self.get_values()

        # save the config to file
        with open('pyvicky/configs/settings.ini', 'w') as f:
            self.settings.write(f)
            logging.info('Settings saved')
        # save the config to file
        with open(self.settings['Editor']['theme'], 'w') as f:
            self.config.write(f)

        self.accept()

        # close the dialog
        self.destroy()

    def cancel(self):
        self.reject()
        self.destroy()


# TODO: create font preferences dialog
class FontPreferencesDlg(QDialog):
    def __init__(self, parent=None):
        super(FontPreferencesDlg, self).__init__(parent)


class Connector(QObject):

    # Define a new signal called 'trigger' that has no arguments.
    trigger = pyqtSignal()

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        self.trigger.connect(self.handle_trigger)

        # Emit the signal.
        self.trigger.emit()

    def handle_trigger(self):
        # Show that the slot has been called.
        logging.info("trigger signal received")
