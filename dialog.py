#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Callable, Any, Dict
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QHBoxLayout
from PyQt5.QtWidgets import QDialogButtonBox, QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox
from PyQt5 import uic

from bindings import *


# ++++++++++++++++++++++++++++++++++++++++++++++++++

class Dialog(QDialog):
    def __init__(self, ui_pathnfile: str, bindingList: Bindings = None):
        super(Dialog, self).__init__()
        self.__bindingList = None
        self.__validationCallback: Callable[[List[Binding]], bool] = None

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
        self.__bindingList = bindingList
        bindingList.models2widgets()

    def getBindings(self):
        return self.__bindingList

    def value(self, objectName: str) -> Any:
        """ Get the value of a specified input widget.
        The widget is specified by its objectName as given in Qt Designer
        """
        for b in self.__bindingList:
            if b.objectName == objectName:
                return b.getFnc()

    def getChanges(self) -> List[Binding]:
        if self.__bindingList is not None:
            return self.__bindingList.getChanges()
        return Bindings()

    def setCurrentComboItem(self, objectName: str, itemText: str) -> None:
        for w in self.children():
            if w.objectName() == objectName:
                cnt: int = w.count()
                for i in range(0, cnt):
                    if w.itemText(i) == itemText:
                        w.setCurrentIndex(i)
                        return

    def setValidationCallback(self, callback: Callable[[List[Binding]], bool]):
        self.__validationCallback = callback

    def accept(self):
        ok = True
        changes = self.getChanges()
        if len(changes) == 0:
            # close dialog:
            QDialog.accept(self)
        else:
            # validate changes:
            if self.__validationCallback is not None:
                ok = self.__validationCallback(self.getChanges())

            if ok:
                # transfer data from view to model:
                self.__bindingList.widgets2models()
                # close dialog:
                QDialog.accept(self)

# +++++++++++++++++++++++++++++++++++++++++++++++++++
