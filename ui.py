#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox, QHBoxLayout, \
    QDialogButtonBox, QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QComboBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import uic
from dialog import Dialog
#from mietecontroller import MieteController
#from models import Rechnung, RechnungItem

#++++++++++++++++++++++++++++++++++++++++++++++++++

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

    def onDeleteMiete(self):
        self.__controller.onDeleteMiete()

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
        self.__controller.onMietenEdit()

    # def onAdjustMieteClicked(self):
    #     self.__controller.onAdjustMieteClicked()

    def onNewHausgeldClicked(self):
        self.__controller.onNewHausgeld()

    def onEditHausgeldClicked(self):
        self.__controller.onEditHausgeld()

    def onDeleteHausgeldClicked(self):
        self.__controller.onDeleteHausgeld()

    def showError(self, text, details = None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        if details:
            msg.setDetailedText( details )
        msg.setStandardButtons(QMessageBox.Abort)
        msg.exec_()

    def showInformation(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

#++++++++++++++++++++++++++++++++++++++++++++++++++

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

#++++++++++++++++++++++++++++++++++++++

class WvDialog( Dialog): #replace by MyDialog
    def __init__(self, ui_file):
        super(WvDialog, self).__init__(ui_file)

    def setWohnungIdent(self, ident):
        self.lblWohnung.setText(ident) #ensure to have a QLabel "lblWohnung"

    # #tool button "show calendar" for Gueltig Ab clicked:
    # def onTbGueltigAbClicked(self):
    #     #self.__controller.onShowCalendarForRechnungsdatum()
    #     pass
    #
    # # tool button "show calendar" for Gueltig Bis clicked:
    # def onTbGueltigBisClicked(self):
    #     # self.__controller.onShowCalendarForRechnungsdatum()
    #     pass

#+++++++++++++++++++++++++++++++++++++++

class MieteDialog(WvDialog):
    def __init__(self, mieteController):
        super(MieteDialog, self).__init__("miete31.ui")
        self.__mieteController = mieteController
        val = QDoubleValidator(0, 9999, 2)
        self.inNettoMiete.setValidator(val)
        self.inNettoMiete_neu.setValidator(val)
        self.inNkAbschlag.setValidator(val)
        self.inNkAbschlag_neu.setValidator(val)


    def onDatumReset(self):
        senderName = self.sender().objectName()
        self.__mieteController.resetDate(senderName)

    def onMieteGueltigAbClicked(self):
        senderName = self.sender().objectName()
        self.__mieteController.onShowCalendarForGueltigAb(senderName)

    def onMieteGueltigBisClicked(self):
        senderName = self.sender().objectName()
        self.__mieteController.onShowCalendarForGueltigBis(senderName)

#+++++++++++++++++++++++++++++++++++++++

class HausgeldDialog(WvDialog):
    def __init__(self, hausgeldController):
        super(HausgeldDialog, self).__init__("hausgeld.ui")
        self.__hausgeldController = hausgeldController
        val = QDoubleValidator(0, 9999, 2)
        self.inHausgeldAbschlag.setValidator(val)
        self.inDavonRuecklage.setValidator(val)
        self.inHausgeldAbschlag.selectAll()
        self.inHausgeldAbschlag.setFocus()

    def onDatumReset(self):
        senderName = self.sender().objectName()
        self.__hausgeldController.resetDate(senderName)

    def onHausgeldGueltigAbClicked(self):
        senderName = self.sender().objectName()
        self.__hausgeldController.onShowCalendar(senderName)

    def onHausgeldGueltigBisClicked(self):
        senderName = self.sender().objectName()
        self.__hausgeldController.onShowCalendar(senderName)

#++++++++++++++++++++++++++++++++++++++++++++++++

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
        self.done( self.calendar.selectedDate().toJulianDay() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++
