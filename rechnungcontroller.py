#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from PyQt5.QtCore import Qt, QVariant, QDate
from ui import RechnungDlg, CalendarDlg
from business import DataProvider, ServiceError
from models import Rechnung

class RechnungController:

    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider
        self.__rechnungDlg = None

    def editRechnung(self, whg_short, rechnung): #rechnung: type of Rechnung
        self.__rechnungDlg = RechnungDlg(self, rechnung)
        self.__rechnungDlg.setWohnungIdent(whg_short)
        if self.__rechnungDlg.exec_() > 0:
            resp = self.__dataProvider.updateRechnung( rechnung.rechnungDictionary() )
            if resp.rc() == 0:
                return True
        return False

    def newRechnung(self, whg_short, rechnung):
        self.__rechnungDlg = RechnungDlg(self, rechnung)
        self.__rechnungDlg.setWohnungIdent( whg_short )
        if self.__rechnungDlg.exec_() > 0:
            retVal = self.__dataProvider.insertRechnung(rechnung.rechnungDictionary())
            rechnung.setValue( 'rg_id', retVal.object_id() )

    def onShowCalendarForRechnungsdatum(self):
        rechngDatum = self.__rechnungDlg.inRgDatum.text()
        olddate = QDate.fromString( rechngDatum, "yyyy-MM-dd" )
        retval = self.__showCalendar( olddate )
        if type( retval ) == QDate:
            self.__rechnungDlg.inRgDatum.setText(retval.toString("yyyy-MM-dd"))

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

    def __showCalendar(self, startDate ):
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate(startDate)
        retVal = cal.exec_()
        if retVal > 0:
            return QDate.fromJulianDay( retVal )
        else: return QVariant