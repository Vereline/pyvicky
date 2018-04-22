# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QErrorMessage
import logging
import configparser


class BaseHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(BaseHighlighter, self).__init__(parent)

        self.parent = parent
        self.indenters = []
        self.dedenters = []

    def get_palette(self):
        raise NotImplementedError('You must subclass BaseHighlighter and implement this function.'
                                  ' It should return a QtGui.QPalette.')


class PythonHighlighter(BaseHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.parent = parent
        self.load_config()

        self.classRegex = QtCore.QRegExp("\\bQ[A-Za-z]+\\b")
        self.singleLineCommentRegex = QtCore.QRegExp("#[^\n]*")
        self.multiLineCommentRegex = None
        self.singleQuoteRegex = QtCore.QRegExp("'.*'")
        self.doubleQuoteRegex = QtCore.QRegExp("\".*\"")
        self.functionRegex = QtCore.QRegExp("\\b[A-Za-z0-9_]+(?=\\()")
        self.commentStartRegex = QtCore.QRegExp('/"""')
        self.commentEndRegex = QtCore.QRegExp('"""/')

        self.commentChar = '#'

        keyword_format = QtGui.QTextCharFormat()
        keyword_format.setFontWeight(QtGui.QFont.Bold)
        self.keywordPatterns = self.get_patterns('pyvicky/keywords/python_keywords.txt')
        self.highlightingRules = [(QtCore.QRegExp(pattern), keyword_format)
                                  for pattern in self.keywordPatterns]

        class_format = QtGui.QTextCharFormat()
        class_format.setFontWeight(QtGui.QFont.Bold)
        self.highlightingRules.append((self.classRegex,
                                       class_format))

        single_line_comment_format = QtGui.QTextCharFormat()
        self.highlightingRules.append((self.singleLineCommentRegex, single_line_comment_format))

        self.multiLineCommentFormat = QtGui.QTextCharFormat()

        quotation_format = QtGui.QTextCharFormat()
        self.highlightingRules.append((self.doubleQuoteRegex,
                                       quotation_format))
        self.highlightingRules.append((self.singleQuoteRegex,
                                       quotation_format))

        function_format = QtGui.QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QtCore.Qt.blue)
        self.highlightingRules.append((self.functionRegex,
                                       function_format))

        self.commentStartExpression = self.commentStartRegex
        self.commentEndExpression = self.commentEndRegex

        # For use by the main editor
        self.indenters = ['def', 'for', 'while', 'do', 'class', 'if', 'else', 'elif', 'switch', 'case', 'try',
                          'except', 'finally']
        self.dedenters = ['break', 'continue', 'return']

    def highlightBlock(self, text):
        for pattern, _format in self.highlightingRules:
            expression = QtCore.QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, _format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.commentStartExpression.indexIn(text)

        while start_index >= 0:
            end_index = self.commentEndExpression.indexIn(text, start_index)

            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + self.commentEndExpression.matchedLength()

            self.setFormat(start_index, comment_length, self.multiLineCommentFormat)
            start_index = self.commentStartExpression.indexIn(text, start_index + comment_length)

    @staticmethod
    def get_patterns(file_path):
        patterns = []
        with open(file_path, 'r') as f:
            for keyword in f:
                patterns.append('\\b{}\\b'.format(keyword.strip()))
        return patterns

    def load_config(self):
        self.settings = configparser.ConfigParser()
        self.settings.read('pyvicky/configs/settings.ini')
        self.theme = configparser.ConfigParser()  # The theme config
        try:
            self.theme.read(self.settings['Editor']['theme'])
        except Exception as e:
            logging.error(e)
            self.theme.read('pyvicky/configs/themes/default.ini')
            self.make_error_popup(msg='Unable to load theme at path specified in settings.ini. '
                                      'Reverting to default theme.')

    def get_QColor(self, color_string):
        try:
            # Assume the string is hexadecimal RGB
            rVal = int(color_string[:2], 16)
            gVal = int(color_string[2:4], 16)
            bVal = int(color_string[4:6], 16)
            return QtGui.QColor(rVal, gVal, bVal)
        except Exception as e:
            logging.error(e)
            # Not hex string, so try a built-in QColor color
            try:
                return QtGui.QColor('#' + color_string)
            except Exception as e:
                logging.error(e)
                return None

    def get_palette(self):
        palette = QtGui.QPalette()

        # Keywords
        keyword_color = self.get_QColor(self.theme['Colors']['Keyword'])
        if keyword_color:
            keyword_format = QtGui.QTextCharFormat()
            keyword_format.setForeground(keyword_color)
            self.highlightingRules += [(pattern, keyword_format) for pattern in self.keywordPatterns]
        else:
            self.make_error_popup(msg='Unable to load the color for Keyword from settings')

        # Background Color
        bg_color = self.get_QColor(self.theme['Colors']['Background'])
        if bg_color:
            palette.setColor(QtGui.QPalette.Base, bg_color)
        else:
            self.make_error_popup(msg='Unable to load the color for Background from settings')

        # Foreground Color
        fgc = self.get_QColor(self.theme['Colors']['Foreground'])
        if fgc:
            palette.setColor(QtGui.QPalette.Text, fgc)
        else:
            self.make_error_popup(msg='Unable to load the color for Foreground from settings')

        # Single Line Comments
        line_comment_color = self.get_QColor(self.theme['Colors']['SingleLineComment'])
        if line_comment_color:
            line_comment_format = QtGui.QTextCharFormat()
            line_comment_format.setForeground(line_comment_color)
            self.highlightingRules.append((self.singleLineCommentRegex, line_comment_format))
        else:
            self.make_error_popup(msg='Unable to load the color for SingleLineComment from settings')

        # Single Quotes
        single_quote_color = self.get_QColor(self.theme['Colors']['String'])
        if single_quote_color:
            single_quote_format = QtGui.QTextCharFormat()
            single_quote_format.setForeground(single_quote_color)
            self.highlightingRules.append((self.singleQuoteRegex, single_quote_format))
        else:
            self.make_error_popup(msg='Unable to load the color for String from settings')

        # Double Quotes (uses same as single quote string)
        if single_quote_color:
            single_quote_format = QtGui.QTextCharFormat()
            single_quote_format.setForeground(single_quote_color)
            self.highlightingRules.append((self.doubleQuoteRegex, single_quote_format))

        # Functions
        function_color = self.get_QColor(self.theme['Colors']['Function'])
        if function_color:
            function_format = QtGui.QTextCharFormat()
            function_format.setForeground(function_color)
            self.highlightingRules.append((self.functionRegex, function_format))
        else:
            self.make_error_popup(msg='Unable to load the color for Function from settings')

        select_color = self.get_QColor(self.theme['Colors']['Highlight'])
        if select_color:
            palette.setColor(QtGui.QPalette.Highlight, select_color)
        else:
            self.make_error_popup(msg='Unable to load the color for Highlight from settings')

        selected_text_color = self.get_QColor(self.theme['Colors']['HighlightedText'])
        if selected_text_color:
            palette.setColor(QtGui.QPalette.HighlightedText, selected_text_color)
        else:
            self.make_error_popup(msg='Unable to load the color for HighlightedText from settings')

        return palette

    @staticmethod
    def make_error_popup(title='Oops', msg='Something went wrong...'):
        popup = QErrorMessage()
        popup.setWindowTitle(title)
        popup.showMessage(msg)


class CppHighlighter(BaseHighlighter):
    def get_palette(self):
        pass
