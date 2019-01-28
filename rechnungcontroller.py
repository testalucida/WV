#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt, QVariant, QDate
from ui import RechnungDlg, CalendarDlg
from business import DataProvider

class RechnungController:

    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider

    def editRechnung(self, whg_short, rg):
        self.__rechnungDlg = RechnungDlg(self, rg)
        self.__rechnungDlg.setWohnungIdent(whg_short)
        if self.__rechnungDlg.exec_() > 0:
            self.__dataProvider.updateRechnung( rg )

    def newRechnung(self, whg_short, rg):
        self.__rechnungDlg = RechnungDlg(self, rg)
        self.__rechnungDlg.setWohnungIdent( whg_short )
        if self.__rechnungDlg.exec_() > 0:
            pass #save new Rechnung

    def onShowCalendarForRechnungsdatum(self):
        cal = CalendarDlg(self)

        cal.exec_()

    def onShowCalendarForRechnungBezahltAm(self):
        bez_am = self.__rechnungDlg.inRgBezahltAm.text()
        olddate = QDate.fromString( bez_am, "yyyy-MM-dd" )
        print( olddate.toString("yyyy-MM-dd"))
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate( olddate )
        retVal = cal.exec_()
        if retVal > 0:
            date = QDate.fromJulianDay(retVal)
            print( date.toString("yyyy-MM-dd") )
            self.__rechnungDlg.inRgBezahltAm.setText( date.toString("yyyy-MM-dd") )