#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import copy
from numbers import Number
from PyQt5.QtCore import Qt, QVariant, QDate
from ui import MieteDialog, CalendarDlg
from business import ValidationError #DataProvider, ServiceError, DataError
#from models import DictTableRow
from bindings import *

class MieteController:

    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider
        self.__mieteDlg = None
        self.__changes: Bindings = None

    def editMiete(self, whg_short,
                  miete: DictTableRow,
                  mieteNewer: DictTableRow = None) -> None:
        """
        :param whg_short:
        :param miete: current or finalized miete record.
        Must be given. Will be displayed in the left part of miete dialog.
        :param mieteNewer: miete record following the miete record given
        by the first parameter.
        If given, will be displayed in the rigth part of miete dialog.
        Might be None.
        Containing a TableItem for each miete data
        :return:
        """

        if mieteNewer is None:
            mieteNewer: DictTableRow = self.__createCopy(miete)
            mieteNewer.setValue('whg_id', miete.value('whg_id'))

        self.__mieteDlg = MieteDialog(self)
        dlg = self.__mieteDlg
        dlg.setValidationCallback(self.validate)
        dlg.setWohnungIdent(whg_short)

        self.__bind(dlg, miete, mieteNewer)

        self.__changes = None
        if dlg.exec_() > 0:
            if mieteNewer.value('miete_id') == '':
                if mieteNewer.value('netto_miete') > '':
                    self.__dataProvider.insertMiete(mieteNewer.dictionary())
            else:
                updateLeft = False;
                updateRight = False;
                for chng in self.__changes:
                    if chng.groupName() == 'left':
                        updateLeft = True
                    if chng.groupName() == 'right':
                        updateRight = True
                    if updateLeft and updateRight:
                        break
                if updateLeft:
                    self.__dataProvider.updateMiete(miete.dictionary())
                if updateRight:
                    self.__dataProvider.updateMiete(mieteNewer.dictionary())

    def __createCopy(self, row: DictTableRow) -> DictTableRow:
        dict_cpy = copy.deepcopy(row.dictionary())
        self.__resetDictionary(dict_cpy)

        return DictTableRow(dict_cpy)

    def __resetDictionary(self, dic: dict):
        for key, val in dic.items():
            if isinstance(val, str):
                dic[key] = ''
            elif isinstance(val, Number):
                dic[key] = 0
            elif isinstance(val, dict):
                self.__resetDictionary(val)
            else:
                #todo: raise exception
                pass

    def __bind(self, dlg: MieteDialog,
               miete: DictTableRow,
               mieteNeu: DictTableRow):

        bs = Bindings()

        bs.startGroup('left')

        b = TextBinding(miete.getItem('netto_miete'),
                        dlg.inNettoMiete.text, dlg.inNettoMiete.setText )
        bs.append(b)

        b = TextBinding(miete.getItem('nk_abschlag'),
                        dlg.inNkAbschlag.text, dlg.inNkAbschlag.setText)
        bs.append(b)

        b = TextBinding(miete.getItem('gueltig_ab'),
                        dlg.inMieteGueltigAb.text, dlg.inMieteGueltigAb.setText)
        bs.append(b)

        b = TextBinding(miete.getItem('gueltig_bis'),
                        dlg.inMieteGueltigBis.text, dlg.inMieteGueltigBis.setText)
        bs.append(b)

        b = TextBinding(miete.getItem('bemerkung'),
                        dlg.txtMieteBemerk.toPlainText, dlg.txtMieteBemerk.setPlainText)
        bs.append(b)

        bs.startGroup('right')

        b = TextBinding(mieteNeu.getItem('netto_miete'),
                        dlg.inNettoMiete_neu.text, dlg.inNettoMiete_neu.setText)
        bs.append(b)

        b = TextBinding(mieteNeu.getItem('nk_abschlag'),
                        dlg.inNkAbschlag_neu.text, dlg.inNkAbschlag_neu.setText)
        bs.append(b)

        b = TextBinding(mieteNeu.getItem('gueltig_ab'),
                        dlg.inMieteGueltigAb_neu.text, dlg.inMieteGueltigAb_neu.setText)
        bs.append(b)

        b = TextBinding(mieteNeu.getItem('gueltig_bis'),
                        dlg.inMieteGueltigBis_neu.text, dlg.inMieteGueltigBis_neu.setText)
        bs.append(b)

        b = TextBinding(mieteNeu.getItem('bemerkung'),
                        dlg.txtMieteBemerk_neu.toPlainText, dlg.txtMieteBemerk_neu.setPlainText)
        bs.append(b)

        dlg.setBindings(bs)

    def onShowCalendarForGueltigAb(self):
        gueltigAb = self.__mieteDlg.inMieteGueltigAb.text()
        olddate = QDate.fromString( gueltigAb, "yyyy-MM-dd" )
        retval = self.__showCalendar( olddate )
        if type( retval ) == QDate:
            self.__mieteDlg.inMieteGueltigAb.setText(retval.toString("yyyy-MM-dd"))

    def onShowCalendarForGueltigBis(self):
        gueltigBis = self.__mieteDlg.inMieteGueltigBis.text()
        olddate = QDate.fromString( gueltigBis, "yyyy-MM-dd" )
        retval = self.__showCalendar( olddate )
        if type( retval ) == QDate:
            self.__mieteDlg.inMieteGueltigBis.setText(retval.toString("yyyy-MM-dd"))

    def __showCalendar(self, startDate ):
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate(startDate)
        retVal = cal.exec_()
        if retVal > 0:
            return QDate.fromJulianDay( retVal )
        else: return QVariant

    def validate(self, bindings: Bindings, changes: Bindings) -> str:
        msg: str = self.validateLeftSide(bindings)
        if len(msg) > 0:
            return msg
        msg = self.validateRightSide(bindings)
        if len(msg) == 0:
            self.__changes = changes
        return msg

    def validateLeftSide(self, bindings: Bindings) -> str:
        #side: str = 'left'
        if bindings.allWidgetValuesZero('left'):
            if bindings.allWidgetValuesZero('right'):
                return ''
            else:
                return 'Wenn die Werte der rechten Seite gefüllt sind, dürfen die der linken Seite ' \
                       'nicht leer sein. Übertragen Sie die Werte auf die linke Seite.'

        if bindings.getWidgetValue('left', 'netto_miete') <= '0':
            return 'Netto-Miete darf nicht 0 sein.'

        if bindings.getWidgetValue('left', 'nk_abschlag') <= '0':
            return 'Nebenkosten-Abschlag darf nicht 0 sein.'

        gueltAb = bindings.getWidgetValue('left', 'gueltig_ab')
        if gueltAb == '':
            return 'Gültig ab darf nicht leer sein.'

        gueltAb = QDate.fromString( gueltAb, "yyyy-MM-dd" )
        if not gueltAb.isValid():
            return 'Gültig ab ist kein gültiges Datumsformat.'

        gueltBis = bindings.getWidgetValue('left', 'gueltig_bis')
        if gueltBis > '':
            gueltBis = QDate.fromString( gueltBis, "yyyy-MM-dd" )
            if not gueltBis.isValid():
                return 'Gültig bis ist kein gültiges Datumsformat.'
            if not gueltBis > gueltAb:
                return 'Wenn Gültig bis angegeben ist, muss es größer sein als Gültig ab.'

        return ''

    def validateRightSide(self, bindings: Bindings) -> str:
        if bindings.allWidgetValuesZero('right'):
                return ''

        if bindings.getWidgetValue('right', 'netto_miete') <= '0':
            return 'Netto-Miete darf nicht 0 sein.'

        if bindings.getWidgetValue('right', 'nk_abschlag') <= '0':
            return 'Nebenkosten-Abschlag darf nicht 0 sein.'

        gueltAb = bindings.getWidgetValue('right', 'gueltig_ab')
        if gueltAb == '':
            return 'Gültig ab darf nicht leer sein.'

        gueltAb = QDate.fromString( gueltAb, "yyyy-MM-dd" )
        if not gueltAb.isValid():
            return 'Gültig ab ist kein gültiges Datumsformat.'

        gueltBisLeft = bindings.getWidgetValue('left', 'gueltig_bis')
        if gueltBisLeft <= '':
            return 'Werte auf der rechten Seite können erst eingetragen' \
                   'werden, wenn auf der linken Seite ein Gültig-bis-Datum ' \
                   'gesetzt wurde.'

        gueltBisLeft = QDate.fromString(gueltBisLeft, "yyyy-MM-dd")
        if gueltBisLeft > gueltAb:
            return 'Gültig bis auf der linken Seite ' \
                   'darf nicht größer sein als Gültig ab auf der rechten Seite.'

        gueltBis = bindings.getWidgetValue('right', 'gueltig_bis')
        if gueltBis > '':
            gueltBis = QDate.fromString( gueltBis, "yyyy-MM-dd" )
            if not gueltBis.isValid():
                return 'Gültig bis ist kein gültiges Datumsformat.'
            if not gueltBis > gueltAb:
                return 'Wenn Gültig bis angegeben ist, ' \
                       'muss es größer sein als Gültig ab.'

        return ''
