#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QHBoxLayout, QDialogButtonBox
from PyQt5 import uic
from models import Rechnung, RechnungItem

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

    def onDeleteRechnungClicked(self):
        self.__controller.onDeleteRechnungClicked()

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

    def onMietenRowDblClicked( self ):
        self.__controller.onMietenTableDblClicked()

    def showError(self, text, details = None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        if details:
            msg.setDetailedText( details )
        msg.setStandardButtons(QMessageBox.Abort)
        msg.exec_()


class RechnungDlg( QDialog ):

    def __init__(self, controller, rechnung = None): #rechnung: type of Rechnung
        super(RechnungDlg, self).__init__()
        self.__controller = controller
        self.__rechnung = rechnung #type of Rechnung (list of RechnungItems)
        uic.loadUi("rechnung.ui", self)
        self.btnBox.layout().setDirection(QHBoxLayout.RightToLeft)
        okbtn = self.btnBox.button(QDialogButtonBox.Ok)
        okbtn.setAutoDefault(True)
        okbtn.setDefault(True)
        cbtn = self.btnBox.button(QDialogButtonBox.Cancel)
        cbtn.setAutoDefault(False)
        cbtn.setDefault(False)

        self.setAttribute(Qt.WA_DeleteOnClose)
        if rechnung:
            self.__data2View()

    def __data2View(self):
        self.lblRgId.setText( self.__rechnung.value('rg_id'))
        self.inRgNr.setText( self.__rechnung.value('rg_nr') )
        self.inRgDatum.setText(self.__rechnung.value('rg_datum'))
        self.inRgBetrag.setText(self.__rechnung.value('betrag'))
        self.inFirma.setText(self.__rechnung.value('firma'))
        self.spinRgVerteilung.setValue( int( self.__rechnung.value('verteilung_jahre') ) )
        self.txtRgBemerk.setPlainText(self.__rechnung.value('bemerkung'))
        self.inRgBezahltAm.setText( self.__rechnung.value('rg_bezahlt_am'))

    def __view2Data(self):
        rg = self.__rechnung
        rg.setValue('rg_nr', self.inRgNr.text())
        rg.setValue('rg_datum', self.inRgDatum.text())
        rg.setValue('betrag', self.inRgBetrag.text())
        rg.setValue('firma', self.inFirma.text())
        rg.setValue('verteilung_jahre', str(self.spinRgVerteilung.value()))
        rg.setValue('bemerkung', self.txtRgBemerk.document().toPlainText())
        rg.setValue('rg_bezahlt_am', self.inRgBezahltAm.text())

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


class MieteDlg( QDialog ):
    def __init__(self, controller, mieteTableRow = None):
        # mieteTableRow: type of DictTableRow containing TableItems
        super(MieteDlg, self).__init__()
        self.__controller = controller
        self.__mieteTableRow = mieteTableRow #type of dictionary (list of DictTableRo)
        uic.loadUi("miete.ui", self)
        self.btnBox.layout().setDirection(QHBoxLayout.RightToLeft)
        okbtn = self.btnBox.button(QDialogButtonBox.Ok)
        okbtn.setAutoDefault(True)
        okbtn.setDefault(True)
        cbtn = self.btnBox.button(QDialogButtonBox.Cancel)
        cbtn.setAutoDefault(False)
        cbtn.setDefault(False)

        self.setAttribute(Qt.WA_DeleteOnClose)
        if mieteTableRow:
            self.__data2View()

    def __data2View(self):
        self.lblMieteId.setText( self.__mieteTableRow.value('whg_id'))
        self.inNettoMiete.setText( self.__mieteTableRow.value('netto_miete') )
        self.inNkAbschlag.setText(self.__mieteTableRow.value('nk_abschlag'))
        self.inMieteGueltigAb.setText(self.__mieteTableRow.value('gueltig_ab'))
        self.txtMieteBemerk.setPlainText(self.__mieteTableRow.value('bemerkung'))

    def __view2Data(self):
        rg = self.__rechnung
        rg.setValue('rg_nr', self.inRgNr.text())
        rg.setValue('rg_datum', self.inRgDatum.text())
        rg.setValue('betrag', self.inRgBetrag.text())
        rg.setValue('firma', self.inFirma.text())
        rg.setValue('verteilung_jahre', str(self.spinRgVerteilung.value()))
        rg.setValue('bemerkung', self.txtRgBemerk.document().toPlainText())
        rg.setValue('rg_bezahlt_am', self.inRgBezahltAm.text())

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
