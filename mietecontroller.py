#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from PyQt5.QtCore import Qt, QVariant, QDate
from ui import MieteDlg, CalendarDlg
from business import DataProvider, ServiceError
from models import Rechnung

class MieteController:

    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider
        self.__mieteDlg = None

    def editMiete(self, whg_short, mieteTableRow):
        #mieteTableRow: instance of DictTableRow
        #containing TableItems for each miete data
        self.__mieteDlg = MieteDlg(self, mieteTableRow)
        self.__mieteDlg.setWohnungIdent(whg_short)
        if self.__mieteDlg.exec_() > 0:
            #resp = self.__dataProvider.updateMiete( ??? )
            #dic = json.loads(resp.content)
            #if dic['rc'] == 0:
            #    return True
            pass
        return False

    def newMiete(self, whg_short, mieteTableRow):
        self.__mieteDlg = MieteDlg(self, mieteTableRow)
        self.__mieteDlg.setWohnungIdent( whg_short )
        if self.__mieteDlg.exec_() > 0:
            #retVal = self.__dataProvider.insertRechnung(rechnung.rechnungDictionary())
            #mieteTableRow.setValue( 'miete_id', retVal.object_id() )
            pass

    def onShowCalendarForGueltigAb(self):
        gueltigBis = self.__mieteDlg.inMieteGueltigAb.text()
        olddate = QDate.fromString( gueltigBis, "yyyy-MM-dd" )
        retval = self.__showCalendar( olddate )
        if type( retval ) == QDate:
            self.__mieteDlg.inMieteGueltigAb.setText(retval.toString("yyyy-MM-dd"))

    def __showCalendar(self, startDate ):
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate(startDate)
        retVal = cal.exec_()
        if retVal > 0:
            return QDate.fromJulianDay( retVal )
        else: return QVariant