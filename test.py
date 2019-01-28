# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rechnung.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RechnungDlg(object):
    def setupUi(self, RechnungDlg):
        RechnungDlg.setObjectName("RechnungDlg")
        RechnungDlg.resize(544, 423)
        self.gridLayout = QtWidgets.QGridLayout(RechnungDlg)
        self.gridLayout.setObjectName("gridLayout")
        self.txtRgBemerk = QtWidgets.QTextEdit(RechnungDlg)
        self.txtRgBemerk.setObjectName("txtRgBemerk")

        self.label_6 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")

        self.label_2 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")

        self.inRgNr = QtWidgets.QLineEdit(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inRgNr.sizePolicy().hasHeightForWidth())
        self.inRgNr.setSizePolicy(sizePolicy)
        self.inRgNr.setObjectName("inRgNr")

        self.label = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")

        self.label_4 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")

        self.inRgBetrag = QtWidgets.QLineEdit(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inRgBetrag.sizePolicy().hasHeightForWidth())
        self.inRgBetrag.setSizePolicy(sizePolicy)
        self.inRgBetrag.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.inRgBetrag.setObjectName("inRgBetrag")

        self.label_5 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")

        self.label_7 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")

        self.inRgDatum = QtWidgets.QLineEdit(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inRgDatum.sizePolicy().hasHeightForWidth())
        self.inRgDatum.setSizePolicy(sizePolicy)
        self.inRgDatum.setObjectName("inRgDatum")

        self.label_3 = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")

        self.btnBox = QtWidgets.QDialogButtonBox(RechnungDlg)
        self.btnBox.setOrientation(QtCore.Qt.Horizontal)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btnBox.setObjectName("btnBox")

        self.lblRgId = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblRgId.sizePolicy().hasHeightForWidth())
        self.lblRgId.setSizePolicy(sizePolicy)
        self.lblRgId.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblRgId.setObjectName("lblRgId")

        self.inFirma = QtWidgets.QLineEdit(RechnungDlg)
        self.inFirma.setObjectName("inFirma")

        self.spinRgVerteilung = QtWidgets.QSpinBox(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinRgVerteilung.sizePolicy().hasHeightForWidth())
        self.spinRgVerteilung.setSizePolicy(sizePolicy)
        self.spinRgVerteilung.setProperty("value", 1)
        self.spinRgVerteilung.setObjectName("spinRgVerteilung")

        self.tbRgDatumCalendar = QtWidgets.QToolButton(RechnungDlg)
        self.tbRgDatumCalendar.setObjectName("tbRgDatumCalendar")

        self.lblWohnung = QtWidgets.QLabel(RechnungDlg)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblWohnung.sizePolicy().hasHeightForWidth())
        self.lblWohnung.setSizePolicy(sizePolicy)
        self.lblWohnung.setMinimumSize(QtCore.QSize(0, 55))
        self.lblWohnung.setMaximumSize(QtCore.QSize(16777215, 55))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(True)
        self.lblWohnung.setFont(font)
        self.lblWohnung.setAutoFillBackground(False)
        self.lblWohnung.setStyleSheet("background-color: rgb(186, 189, 182);")
        self.lblWohnung.setTextFormat(QtCore.Qt.RichText)
        self.lblWohnung.setAlignment(QtCore.Qt.AlignCenter)
        self.lblWohnung.setWordWrap(True)
        self.lblWohnung.setObjectName("lblWohnung")


        self.gridLayout.addWidget(self.lblWohnung, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.lblRgId, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.inRgNr, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.inRgDatum, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.tbRgDatumCalendar, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.gridLayout.addWidget(self.inRgBetrag, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.spinRgVerteilung, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.inFirma, 7, 1, 1, 2)
        self.gridLayout.addWidget(self.label_7, 9, 0, 1, 1)
        self.gridLayout.addWidget(self.txtRgBemerk, 9, 1, 1, 2)

        self.gridLayout.addWidget(self.btnBox, 10, 0, 1, 3)

        self.retranslateUi(RechnungDlg)
        self.btnBox.accepted.connect(RechnungDlg.accept)
        self.btnBox.rejected.connect(RechnungDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(RechnungDlg)

    def retranslateUi(self, RechnungDlg):
        _translate = QtCore.QCoreApplication.translate
        RechnungDlg.setWindowTitle(_translate("RechnungDlg", "Rechnung erfassen/ändern"))
        self.label_6.setText(_translate("RechnungDlg", "Verteilung auf Jahre: "))
        self.label_2.setText(_translate("RechnungDlg", "Rechnung-Nummer: "))
        self.label.setText(_translate("RechnungDlg", "Rechnung-ID:"))
        self.label_4.setText(_translate("RechnungDlg", "Firma:"))
        self.label_5.setText(_translate("RechnungDlg", "Rechnungsdatum: "))
        self.label_7.setText(_translate("RechnungDlg", "Bemerkung: "))
        self.label_3.setText(_translate("RechnungDlg", "Betrag: "))
        self.lblRgId.setText(_translate("RechnungDlg", "0"))
        self.tbRgDatumCalendar.setText(_translate("RechnungDlg", "..."))
        self.lblWohnung.setText(_translate("RechnungDlg", "<html><head/><body><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RechnungDlg = QtWidgets.QDialog()
    ui = Ui_RechnungDlg()
    ui.setupUi(RechnungDlg)
    RechnungDlg.show()
    sys.exit(app.exec_())

