#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import copy
from numbers import Number
from PyQt5.QtCore import Qt, QVariant, QDate
from ui import HausgeldDialog, CalendarDlg
from business import ValidationError #DataProvider, ServiceError, DataError
#from models import DictTableRow
from bindings import *

class HausgeldController:
    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider
        self.__hausgeldDlg = None
        self.__changes: Bindings = None

    def newHausgeld(self, whg_id: str, whg_short: str) -> None:
        hausgeld_dict = {
            'whg_id': 0,
            'hausgeld_id': '0',
            'gueltig_ab': '',
            'gueltig_bis': '',
            'hausgeld_abschlag': '0',
            'davon_ruecklage': '0',
            'bemerkung': ''
        }
        hausgeld_dict['whg_id'] = whg_id
        row = DictTableRow(hausgeld_dict)
        self.__hausgeldDlg = HausgeldDialog(self)
        dlg = self.__hausgeldDlg
        gueltigAb = QDate().currentDate().toString("yyyy-MM-dd")
        dlg.inHausgeldGueltigAb.setText(gueltigAb)
        dlg.setWohnungIdent(whg_short)
        self.__bind(dlg, row)
        dlg.setValidationCallback(self.validate)

        self.__changes = None
        if dlg.exec_() > 0:
            self.__dataProvider.insertHausgeld(hausgeld_dict)
            return row
        return None

    def editHausgeld(self, whg_short: str, hausgeld: DictTableRow) -> None:
        self.__hausgeldDlg = HausgeldDialog(self)
        dlg = self.__hausgeldDlg
        dlg.setWohnungIdent(whg_short)
        self.__bind(dlg, hausgeld)
        dlg.setValidationCallback(self.validate)

        self.__changes = None
        if dlg.exec_() > 0:
            self.__dataProvider.updateHausgeld(hausgeld.dictionary())
            return hausgeld
        return None

    def deleteHausgeld(self, hausgeld_id: str) -> None:
        self.__dataProvider.deleteHausgeld(hausgeld_id)

    def __bind(self, dlg: HausgeldDialog, hausgeld: DictTableRow) -> None:
        bs = Bindings()
        b = TextBinding(hausgeld.getItem('hausgeld_abschlag'),
                        dlg.inHausgeldAbschlag.text, dlg.inHausgeldAbschlag.setText )
        bs.append(b)

        b = TextBinding(hausgeld.getItem('davon_ruecklage'),
                        dlg.inDavonRuecklage.text, dlg.inDavonRuecklage.setText)
        bs.append(b)

        b = TextBinding(hausgeld.getItem('bemerkung'),
                        dlg.txtHausgeldBemerk.toPlainText, dlg.txtHausgeldBemerk.setPlainText)
        bs.append(b)

        b = TextBinding(hausgeld.getItem('gueltig_ab'),
                        dlg.inHausgeldGueltigAb.text, dlg.inHausgeldGueltigAb.setText)
        bs.append(b)

        b = TextBinding(hausgeld.getItem('gueltig_bis'),
                        dlg.inHausgeldGueltigBis.text, dlg.inHausgeldGueltigBis.setText)
        bs.append(b)

        dlg.setBindings(bs)

    def validate(self, bindings: Bindings, changes: Bindings) -> str:
        if bindings.allWidgetValuesZero():
                return ''

        hausgeldAbschlag = bindings.getWidgetValue(key = 'hausgeld_abschlag')
        if hausgeldAbschlag <= '0':
            return 'Hausgeld-Abschlag darf nicht 0 sein.'

        davonRuecklage = bindings.getWidgetValue('davon_ruecklage')
        if davonRuecklage <= '0':
            return 'Rücklage darf nicht 0 sein.'

        if float(hausgeldAbschlag) < float(davonRuecklage):
            return 'Der Anteil der Rücklage darf nicht größer sein als das Hausgeld selbst.'

        gueltigAb = bindings.getWidgetValue('gueltig_ab')
        if gueltigAb == '':
            return 'Gültig ab muss ein gültiges Datum enthalten.'

        gueltigAb = QDate.fromString(gueltigAb, "yyyy-MM-dd")
        if not gueltigAb.isValid():
            return 'Gültig ab ist kein gültiges Datumsformat.'

        gueltigBis = bindings.getWidgetValue('gueltig_bis')
        if gueltigBis > '':
            gueltBis = QDate.fromString(gueltigBis, "yyyy-MM-dd")
            if not gueltBis.isValid():
                return 'Gültig bis ist kein gültiges Datumsformat.'
            if not gueltBis > gueltigBis:
                return 'Wenn Gültig bis angegeben ist, muss es größer sein als Gültig ab.'

        return ''

    def onShowCalendar(self, senderName: str):
        if senderName == 'tbHausgeldGueltigAb':
            gueltigAb = QDate.fromString(self.__hausgeldDlg.inHausgeldGueltigAb.text(), "yyyy-MM-dd" )
        else: #'tbHausgeldGueltigBis'
            tmp = self.__hausgeldDlg.inMieteGueltigBis.text()
            #todo: do we need to handle gueltigBis explicitly?

        retval = self.__showCalendar( gueltigAb )

        if type( retval ) == QDate:
            if senderName == 'tbHausgeldGueltigAb':
                self.__hausgeldDlg.inHausgeldGueltigAb.setText(retval.toString("yyyy-MM-dd"))
            else:
                self.__hausgeldDlg.inHausgeldGueltigBis.setText(retval.toString("yyyy-MM-dd"))

    def __showCalendar(self, startDate ) -> QDate or None:
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate(startDate)
        retVal = cal.exec_()
        if retVal > 0:
            return QDate.fromJulianDay( retVal )
        else: return None

    def resetDate(self, senderName: str):
        if senderName == 'tbResetHausgeldGueltigAb':
            self.__hausgeldDlg.inHausgeldGueltigAb.setText('')
        elif senderName == 'tbResetHausgeldGueltigBis':
            self.__hausgeldDlg.inHausgeldGueltigBis.setText('')