#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Any, Callable, List, Dict
from PyQt5.QtWidgets import QRadioButton
# from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QDialogButtonBox
# from PyQt5 import uic
from models import TableItem, DictTableRow


# ++++++++++++++++++++++++++++++++++++++++

class Binding:

    def __init__(self,
                 modelKey: str,
                 getModelValue: Callable[[], Any],
                 setModelValue: Callable[[Any], None],
                 getWidgetValue: Callable[[], Any],
                 setWidgetValue: Callable[[Any], None]):
        self.key = modelKey  # key of dictionary entry
        self.getModelValue = getModelValue  # function to get model's value
        self.setModelValue = setModelValue  # function to set model's value
        self.getWidgetValue = getWidgetValue  # function to get widget's value
        self.setWidgetValue = setWidgetValue  # function to set widget's value

    def setBindingParms(self,
                        modelKey: str,
                        getModelValue: Callable[[], Any],
                        setModelValue: Callable[[Any], None],
                        getWidgetValue: Callable[[], Any],
                        setWidgetValue: Callable[[Any], None]):
        self.key = modelKey  # key of dictionary entry
        self.getModelValue = getModelValue
        self.setModelValue = setModelValue
        self.getWidgetValue = getWidgetValue  # function to get widget's value
        self.setWidgetValue = setWidgetValue  # function to set widget's value

    def model2widget(self):
        val = self.getModelValue()
        self.setWidgetValue(val)

    def widget2model(self):
        self.setModelValue(self.getWidgetValue())

    def changed(self) -> bool:
        w = self.getWidgetValue()
        m = self.getModelValue()
        return w != m


# ++++++++++++++++++++++++++++++++++++++++++++

class TextBinding(Binding):
    def __init__(self,
                 tableItem: TableItem,
                 getWidgetValue: Callable[[], Any],
                 setWidgetValue: Callable[[Any], None]):
        super(TextBinding, self).__init__(
            tableItem.key(),
            tableItem.value,
            tableItem.setValue,
            getWidgetValue,
            setWidgetValue)


# ++++++++++++++++++++++++++++++++++++++++++++

class IntBinding(Binding):
    def __init__(self,
                 tableItem: TableItem,
                 getWidgetValue: Callable[[], Any],
                 setWidgetValue: Callable[[int], None]):
        super(IntBinding, self).__init__(
            tableItem.key(),
            tableItem.intValue,
            tableItem.setNumValue,
            getWidgetValue,
            setWidgetValue)


# ++++++++++++++++++++++++++++++++++++++++++++

class FloatBinding(Binding):
    def __init__(self,
                 tableItem: TableItem,
                 getWidgetValue: Callable[[], Any],
                 setWidgetValue: Callable[[float], None]):
        super(FloatBinding, self).__init__(
            # Binding.__init__(self,
            tableItem.key(),
            tableItem.floatValue,
            tableItem.setNumValue,
            getWidgetValue,
            setWidgetValue)


# +++++++++++++++++++++++++++++++++++++++++++++

class ComboBinding(Binding):
    def __init__(self,
                 tableItem: TableItem,
                 getWidgetValue: Callable[[], Any],
                 setWidgetValue: Callable[[str, str], None]):
        super(ComboBinding, self).__init__(
            tableItem.key(),
            tableItem.value,
            tableItem.setValue,
            getWidgetValue,
            setWidgetValue)

    def model2widget(self):
        val = self.getModelValue()
        self.setWidgetValue(self.key, val)


# +++++++++++++++++++++++++++++++++++++++++++++

class RadioMapping:
    """
    RadioButtons represent possible values of a data item.
    So we have to map multiple widgets to only one model entry.
    Furthermore, we have to translate the stored value (typically a char or a digit)
    into displayable text and re-translate the text changed by the user
    into a storable char or digit.
    Example:
    The value range to store gender is {m, f, d}. The displayed text in
    a TableView is {male, female, dunno}. From DB we read "f", which is to be displayed
    as "female" in the TableView. Hence we have to convert "f" to "female".
    To change a row of the table we want to use a dialog, to which we pass the gender
    attribute as "female" (as displayed).
    All gender options are represented by a radio button.
    In the dialog, the "female" radio button has to be checked,
    the "male" and "dunno" radio buttons have to be unchecked.

    By using this class we assign the text displayed in a TableView ("female") to
    its key ("f") and to the radio button controlling the female option.
    """

    def __init__(self,
                 key: str,  # e.g. "f"
                 text: str,  # e.g. "female"
                 radioButton):
        self.key = key
        self.text = text
        self.radioButton = radioButton


# +++++++++++++++++++++++++++++++++++++++++++++

class RadioGroupBinding(Binding):
    # comments based on a gender example:
    # model (dictionary, database): key='gender' value='f'
    # value range: {m, f, d}
    # table display (tableItem.text()): male
    # display range: {male, female, dunno}
    # 3 radiobuttons named rbM, rbF, rbD (objectNames in Qt Designer)
    def __init__(self,
                 tableItem: TableItem,  # "male"
                 radioMappingList: List[RadioMapping]):
        super(RadioGroupBinding, self).__init__(
            tableItem.key(),
            tableItem.value,
            tableItem.setValue,
            self.getWidgetValue,
            self.setWidgetValue)

        self.__radioMappingList = radioMappingList

    def getWidgetValue(self) -> str:
        """
        we simulate *one* widget: iterate through all
        radio buttons and return the mapped key of the
        checked radio button (there is only one).
        """
        for m in self.__radioMappingList:
            if m.radioButton.isChecked():
                return m.key

    def setWidgetValue(self, value: str):
        for m in self.__radioMappingList:
            if m.key == value or m.text == value:
                m.radioButton.setChecked(True)
            else:
                m.radioButton.setChecked(False)

    # def model2widget(self):
    #     val = self.getModelValue()
    #     for m in self.__radioMappingList:
    #         if m.key == val:
    #             m.radioButton.setChecked(True)
    #         else:
    #             m.radioButton.setChecked(False)

    def widget2model(self):
        for m in self.__radioMappingList:
            if m.radioButton.isChecked():
                self.setModelValue(m.key)


# +++++++++++++++++++++++++++++++++++++++++++++

class Bindings(list):
    def __init__(self):
        pass

    def models2widgets(self):
        for b in self:
            b.model2widget()

    def widgets2models(self):
        for b in self:
            b.widget2model()

    def getChanges(self) -> List[Binding]:
        l = list()
        for b in self:
            if b.changed():
                l.append(b)

        return l

# +++++++++++++++++++++++++++++++++++++++++++++++
