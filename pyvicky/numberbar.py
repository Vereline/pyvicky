# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit, QCompleter
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QTextCursor

import logging
import configparser
import os
import sys


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        self.completer = None
        completer = QAutoComplete()
        self.setCompleter(completer)
        self.moveCursor(QTextCursor.End)

        logging.info('Create editor with number bar')

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    # TODO: make this feature optional
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)  # change it and make more transparent
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer = completer
        self.completer.activated.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) -
                 len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[len(completion) - extra:len(completion)])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (
                    Qt.Key_Enter,
                    Qt.Key_Return,
                    Qt.Key_Escape,
                    Qt.Key_Tab,
                    Qt.Key_Backtab):
                event.ignore()
                return

        isShortcut = (event.modifiers() == Qt.ControlModifier and
                      event.key() == Qt.Key_E)
        if not self.completer or not isShortcut:
            QPlainTextEdit.keyPressEvent(self, event)

        ctrlOrShift = event.modifiers() in (Qt.ControlModifier,
                                            Qt.ShiftModifier)
        if ctrlOrShift and event.text() is '':
            # ctrl or shift key on it's own
            return

        eow = str("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=")  # end of word

        hasModifier = ((event.modifiers() != Qt.NoModifier) and
                       not ctrlOrShift)

        completionPrefix = self.textUnderCursor()

        if (not isShortcut and (hasModifier or event.text() is '' or
                                len(completionPrefix) < 2 or
                                (event.text()[-1]) in eow)):
            self.completer.popup().hide()
            return

        if completionPrefix != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(completionPrefix)
            popup = self.completer.popup()
            popup.setCurrentIndex(
                self.completer.completionModel().index(0, 0))

        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                    + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)


class QAutoComplete(QCompleter):
    # TODO: after setting new keyword setting you need to reload program to get new dictionary
    def __init__(self, parent=None):
        words = []
        self.settings = configparser.ConfigParser()
        self.settings.read('pyvicky/configs/settings.ini')
        try:
            str_path = self.settings['Dictionary']['path']
            with open(str_path, "r") as f:
                for word in f:
                    words.append(word.strip())
                f.close()
        except IOError as e:
            logging.error("unable to load keyword dictionary")
            logging.error(e)
            logging.error(os.getcwd())
            try:
                f = open("/usr/share/dict/words", "r")  # default system dict
                for word in f:
                    words.append(word.strip())
                f.close()
            except IOError:
                logging.error("dictionary not in anticipated location")
        QCompleter.__init__(self, words, parent)
