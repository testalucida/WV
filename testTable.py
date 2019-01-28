#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from ui import MainWindow

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("testTable.ui", self)

class TableModel(QStandardItemModel ):
    def __init__(self):
        QStandardItemModel.__init__(self)
        # each row of a tableview is represented by a
        # list of QStandardItem
        row = []
        item = QStandardItem( "item1" )
        row.append( item )
        item = QStandardItem("item2")
        row.append(item)
        item = QStandardItem("item3")
        row.append(item)
        self.appendRow( row )

        row2 = []
        item = QStandardItem( "item1" )
        row2.append( item )
        item = QStandardItem("item2")
        row2.append(item)
        item = QStandardItem("item3")
        row2.append(item)

        self.appendRow( row2 )

        # for i in range(3):
        #     item = QStandardItem( "item" )
        #     self.appendRow( item )
    #
    # def data(self, idx, role=None):
    #     data = self.itemData(idx)
    #     return data

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    model = TableModel()
    window.tv.setModel( model )

    window.show()
    sys.exit(app.exec_())