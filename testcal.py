# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Calendar.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(474, 282)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.calendar = QtWidgets.QCalendarWidget(Dialog)
        self.calendar.setObjectName("calendar")
        self.gridLayout.addWidget(self.calendar, 0, 0, 1, 1)
        self.btnBox = QtWidgets.QDialogButtonBox(Dialog)
        self.btnBox.setOrientation(QtCore.Qt.Horizontal)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnBox.setObjectName("btnBox")
        self.gridLayout.addWidget(self.btnBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.btnBox.accepted.connect(Dialog.accept)
        self.btnBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #date = QDate(QDate.fromString( "2017-01-01", "yyyy-MM-dd"))
        #date = QDate(2017, 1, 1)
        date = QDate.fromString("2017-01-01", "yyyy-MM-dd")
        self.calendar.setSelectedDate(date)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

