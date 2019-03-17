# -*- coding: utf-8 -*-

from typing import Dict, Any, Callable
from PyQt5.QtWidgets import QApplication
from dialog import DictBindingDialog
from models import TableItem, DictTableRow

dic = {
    'str': 'bin ein String',
    'nr': '123',
    'spin': '7'
}



class TestInputDialog(DictBindingDialog):
    def __init__(self):
        super(TestInputDialog, self).__init__("testInput.ui")
        self.__tableRow: DictTableRow = None

    def setTableRow(self, row: DictTableRow):
        self.__tableRow = row
        self.__bind()

    def __bind(self):
        self.bind("inStr",
                  self.inStr.text,
                  self.inStr.setText,
                  'str',
                  dic['str'])
        self.bind("inNr",
                  self.inNr.text,
                  self.inNr.setText,
                  'nr',
                  dic['nr'])
        self.bind("inSpin",
                  self.inSpin.value,
                  self.inSpin.setValue,
                  'spin',
                  int(dic['spin']))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    #create the model assuming it's a table's row
    tableRow = DictTableRow(dic)
    #create dialog
    dlg = TestInputDialog()
    #set dialog's model
    dlg.setTableRow(tableRow)

    dlg.inCombo.addItem("")
    dlg.inCombo.addItem("red")
    dlg.inCombo.addItem("yellow")
    dlg.inCombo.addItem("green")
    dlg.inCombo.addItem("blue")
    dlg.inCombo.setCurrentIndex(2)


    dlg.show()
    sys.exit(app.exec_())
