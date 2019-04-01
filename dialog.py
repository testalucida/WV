#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable, Any, Dict
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QMessageBox
from PyQt5.QtWidgets import QDialogButtonBox, QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox
from PyQt5 import uic

from bindings import *


# ++++++++++++++++++++++++++++++++++++++++++++++++++

class Dialog(QDialog):
    def __init__(self, ui_pathnfile: str, bindingList: Bindings = None):
        super(Dialog, self).__init__()
        self.__bindings = None
        #self.__validationCallback: Callable[[List[Binding]], bool] = None
        self.__validationCallback: Callable[[Bindings, Bindings], str] = None

        uic.loadUi(ui_pathnfile, self)

        # important: Buttonbox' name has to be 'buttonBox'
        self.buttonBox.layout().setDirection(QHBoxLayout.RightToLeft)
        okbtn = self.buttonBox.button(QDialogButtonBox.Ok)
        okbtn.setAutoDefault(True)
        okbtn.setDefault(True)
        cbtn = self.buttonBox.button(QDialogButtonBox.Cancel)
        cbtn.setAutoDefault(False)
        cbtn.setDefault(False)

        self.setAttribute(Qt.WA_DeleteOnClose)

        if bindingList is not None:
            self.setBindings(bindingList)

    def setBindings(self, bindingList: Bindings):
        self.__bindings = bindingList
        bindingList.models2widgets()

    def getBindings(self):
        return self.__bindings

    def value(self, objectName: str) -> Any:
        """ Get the value of a specified input widget.
        The widget is specified by its objectName as given in Qt Designer
        """
        for b in self.__bindings:
            if b.objectName == objectName:
                return b.getFnc()

    def getChanges(self) -> Bindings:
        if self.__bindings is not None:
            return self.__bindings.getChanges()
        return Bindings()

    def setCurrentComboItem(self, objectName: str, itemText: str) -> None:
        for w in self.children():
            if w.objectName() == objectName:
                cnt: int = w.count()
                for i in range(0, cnt):
                    if w.itemText(i) == itemText:
                        w.setCurrentIndex(i)
                        return

    def setValidationCallback(self, callback: Callable[[Bindings, Bindings], str]):
        self.__validationCallback = callback

    def showError(self, text, details = None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        if details:
            msg.setDetailedText( details )
        msg.setStandardButtons(QMessageBox.Abort)
        msg.exec_()

    def accept(self):
        changes = self.getChanges()
        if len(changes) == 0:
            # close dialog:
            QDialog.close(self)
        else:
            # validate changes:
            if self.__validationCallback is not None:
                msg: str = \
                    self.__validationCallback(self.__bindings, changes)
                if len(msg) > 0:
                    self.showError(msg)
                    return

            #now transfer widgets' values to model
            self.__bindings.widgets2models()
            # close dialog:
            QDialog.accept(self)



# +++++++++++++++++++++++++++++++++++++++++++++++++++
