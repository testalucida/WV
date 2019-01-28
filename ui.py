#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QHBoxLayout, QDialogButtonBox
from PyQt5 import uic


class MainWindow(QMainWindow):
    __controller = None
    __hiddenRows = []

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("WvMainWindow3.ui", self)

    def set_controller(self, controller):
        self.__controller = controller

    def onWohnungenTreeClicked(self):
        self.__controller.onWohnungenTreeClicked()

    def onTabsWohnungClicked(self, index):
        print( "onTabsWohnungClicked: ", index )

    def onNewRechnungClicked( self ):
        #print( "onNewRechnungClicked" )
        self.__controller.onNewRechnungClicked()

    def onRechnungenRowDblClicked( self ):
        self.__controller.onRechnungenTableDblClicked()

    # def onFilterRechnungenClicked(self):
    #     self.__controller.onFilterRechnungenClicked()

    def onTestClicked(self):
        self.__controller.onTestClicked()

    def onRechnungenFilterChanged(self):
        self.__controller.onRechnungenFilterChanged()

    def onRechnungDataChanged(self):
        pass  #todo

    def hideTableRechnungenRow(self, rows):
        for row in rows:
            self.tblRechnungen.hideRow(row)
            self.__hiddenRows.append(row)

    def clearFilter(self):
        for row in self.__hiddenRows:
            self.tblRechnungen.showRow(row)
        self.__hiddenRows.clear()

    def showError(self, text, details = None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        if details:
            msg.setDetailedText( details )
        msg.setStandardButtons(QMessageBox.Abort)
        msg.exec_()


class RechnungDlg( QDialog ):

    def __init__(self, controller, rg = None):
        super(RechnungDlg, self).__init__()
        self.__controller = controller
        self.__rg = rg
        uic.loadUi("rechnung.ui", self)
        self.btnBox.layout().setDirection(QHBoxLayout.RightToLeft)
        okbtn = self.btnBox.button(QDialogButtonBox.Ok)
        okbtn.setAutoDefault(True)
        okbtn.setDefault(True)
        cbtn = self.btnBox.button(QDialogButtonBox.Cancel)
        cbtn.setAutoDefault(False)
        cbtn.setDefault(False)

        self.setAttribute(Qt.WA_DeleteOnClose)
        if rg:
            self.__data2View()

    def __data2View(self):
        self.lblRgId.setText( self.__rg['rg_id'])
        self.inRgNr.setText( self.__rg['rg_nr'] )
        self.inRgDatum.setText(self.__rg['rg_datum'])
        self.inRgBetrag.setText(self.__rg['betrag'])
        self.inFirma.setText(self.__rg['firma'])
        self.spinRgVerteilung.setValue( int( self.__rg['verteilung_jahre'] ) )
        self.txtRgBemerk.setPlainText(self.__rg['bemerkung'])
        self.inRgBezahltAm.setText( self.__rg['rg_bezahlt_am'])

    def __view2Data(self):
        rg = self.__rg
        rg['rg_nr'] = self.inRgNr.text()
        rg['rg_datum'] = self.inRgDatum.text()
        rg['betrag'] = self.inRgBetrag.text()
        rg['firma'] = self.inFirma.text()
        rg['verteilung_jahre'] = str(self.spinRgVerteilung.value())
        rg['bemerkung'] = self.txtRgBemerk.document().toPlainText()
        rg['rg_bezahlt_am'] = self.inRgBezahltAm.text()

    def setWohnungIdent(self, ident ):
        self.lblWohnung.setText( ident )

    #tool button "show calendar" for RgDatum clicked:
    def onTbRgDatumCalendarClicked(self):
        self.__controller.onShowCalendarForRechnungsdatum()

    # tool button "show calendar" for Bezahlt am clicked:
    def onTbRgBezahltAmCalendarClicked(self):
        self.__controller.onShowCalendarForRechnungBezahltAm()

    def accept(self):
        self.__view2Data()
        #close dialog:
        QDialog.accept( self )


class CalendarDlg(QDialog):
    __controller = None

    def __init__(self, controller ):
        super(CalendarDlg,self).__init__()
        __controller = controller
        uic.loadUi("Calendar.ui", self)
        self.btnBox.layout().setDirection(QHBoxLayout.RightToLeft)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.calendar.clicked[QDate].connect(self.showDate)

    def showDate(self):
        print( self.calendar.selectedDate().toJulianDay() )

    def accept(self):
        #close dialog:
        QDialog.accept( self )
        print( "accept" )
        self.done( self.calendar.selectedDate().toJulianDay() )
