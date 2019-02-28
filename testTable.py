# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testTable.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import QVariant, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItem, QStandardItemModel

dict1 = {
    'id': '111',
    'netto' : '345,67',
    'nk' : '33,44'
}

dict2 = {
    'id': '222',
    'netto' : '343',
    'nk' : '12'
}

dicList = [dict1, dict2]

#+++++++++++++++++++++++++++++++++++++

class TableItem(QStandardItem):
    def __init__(self, key, value, dictTableRow = None):
        QStandardItem.__init__(self, value)
        self.__key = key
        # the DictTableRow this TableItem belongs to:
        self.__dictTableRow = dictTableRow

    def key(self):
        return self.__key

    def value(self):
        return self.text()

    # returns the DictTableRow this TableItem belongs to
    def dictTableRow(self):
        return self.__dictTableRow

    def setValue(self, newValue ):
        self.setText( newValue )

    def print(self):
        print( "key: ", self.key(), " value: ", self.value() )

#++++++++++++++++++++++++++++++++++++++++

class DictTableRow( list ) :
    def __init__(self, dic):
        self.__dict = dic
        for key, val in dic.items():
            item = TableItem(key, val, self)
            self.append(item)

    def dump(self):
        for item in self:
            item.print()

#++++++++++++++++++++++++++++++++++++++++

class DictListTableModel(QStandardItemModel):

    def __init__(self, dicList):
        QStandardItemModel.__init__(self)
        #self.__dictList = dicList
        headers = False
        for dic in dicList:
            #row = []
            row = DictTableRow( dic )
            # for key, val in dic.items():
            #     item = TableItem(key, val)
            #     row.append(item)

            self.appendRow(row)

            if not headers:
                c = 0
                for key, val in dic.items():
                    self.setHeaderData(c, Qt.Horizontal, key)
                    c += 1
            headers = True

    #returns the DictTableRow the specified item belongs to
    def rowDictionary(self, index):
        tableItem = self.itemFromIndex(index)
        return tableItem.dictTableRow()


#+++++++++++++++++++++++++++++++++++++++


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tv = QtWidgets.QTableView(self.centralwidget)
        self.tv.setObjectName("tv")
        self.gridLayout.addWidget(self.tv, 0, 0, 1, 1)
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setObjectName("btn")
        self.gridLayout.addWidget(self.btn, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btn.clicked.connect(self.onBtnClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def onBtnClicked(self):
        indexes = self.tv.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            item = index.model().itemFromIndex(index)
            #item: TableItem (inherited from QStandardItem)
            print( item.key(), ": ", item.value() )
            item.setValue( "new Value")

            row = item.dictTableRow()
            row.dump()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn.setText(_translate("MainWindow", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    tm = DictListTableModel(dicList)
    ui.tv.setModel(tm)
    MainWindow.show()
    sys.exit(app.exec_())

