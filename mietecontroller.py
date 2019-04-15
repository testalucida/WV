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

    def deleteMiete(self, miete_id: int) -> None:
        """
        deletes the selected miete table entry
        :param miete: miete entry to delete
        :return: None
        """
        self.__dataProvider.deleteMiete(miete_id)

    def insertFirstMiete(self, whg_id: str, whg_short: str) -> DictTableRow:
        """
        inserts the first miete record
        :param whg_id: flat's id
        :param whg_short: flat's address
        :return:
        """
        # create a miete dictionary:
        miete_dict = {
            'whg_id': 0,
            'miete_id': '0',
            'gueltig_ab': '',
            'gueltig_bis': '',
            'netto_miete': '0',
            'nk_abschlag': '0',
            'brutto_miete': '',
            'bemerkung': ''
        }
        miete_dict['whg_id'] = whg_id
        row = DictTableRow(miete_dict)

        self.__mieteDlg = MieteDialog(self)
        dlg = self.__mieteDlg
        dlg.inNettoMiete_neu.setEnabled(False)
        dlg.inNkAbschlag_neu.setEnabled(False)
        dlg.tbMieteGueltigAb_neu.setEnabled(False)
        dlg.tbMieteGueltigBis_neu.setEnabled(False)
        dlg.txtMieteBemerk_neu.setEnabled(False)
        dlg.setValidationCallback(self.validate)
        dlg.setWohnungIdent(whg_short)

        self.__bind(dlg, row)

        self.__changes = None
        if dlg.exec_() > 0:
            self.__dataProvider.insertMiete(miete_dict)
            return row
        return None

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
            insertedRight = False
            if mieteNewer.value('miete_id') == '':
                if mieteNewer.value('netto_miete') > '':
                    self.__dataProvider.insertMiete(mieteNewer.dictionary())
                    insertedRight = True

            updateLeft = False
            updateRight = False
            for chng in self.__changes:
                if chng.groupName() == 'left':
                    updateLeft = True
                if chng.groupName() == 'right':
                    updateRight = True
                if updateLeft and updateRight:
                    break
            if updateLeft:
                self.__dataProvider.updateMiete(miete.dictionary())
            if updateRight and not insertedRight:
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
               mieteNeu: DictTableRow = None) -> None:

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

        if mieteNeu is not None:
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

    def add1Day(self, date: str) -> QDate:
        qdate = QDate.fromString(date, "yyyy-MM-dd")
        if qdate.isValid():
            qdate = qdate.addDays(1)

            return qdate

        return QDate()

    def onShowCalendarForGueltigAb(self, senderName: str):
        if senderName == 'tbMieteGueltigAb':
            gueltigAb = QDate.fromString(self.__mieteDlg.inMieteGueltigAb.text(), "yyyy-MM-dd" )
        else: #'tbMieteGueltigAb_neu'
            tmp = self.__mieteDlg.inMieteGueltigAb_neu.text()
            if len(tmp) < 1:
                gueltigAb = self.add1Day(self.__mieteDlg.inMieteGueltigBis.text())
            else:
                gueltigAb = QDate.fromString(tmp, "yyyy-MM-dd")

        retval = self.__showCalendar( gueltigAb )
        if type( retval ) == QDate:
            if senderName == 'tbMieteGueltigAb':
                self.__mieteDlg.inMieteGueltigAb.setText(retval.toString("yyyy-MM-dd"))
            else:
                self.__mieteDlg.inMieteGueltigAb_neu.setText(retval.toString("yyyy-MM-dd"))

    def onShowCalendarForGueltigBis(self, senderName: str):
        if senderName == 'tbMieteGueltigBis':
            gueltigBis = QDate.fromString(self.__mieteDlg.inMieteGueltigBis.text(), "yyyy-MM-dd" )
        else: #'tbMieteGueltigBis_neu'
            tmp = self.__mieteDlg.inMieteGueltigBis_neu.text()
            if len(tmp) < 1:
                gueltigBis = self.add1Day(self.__mieteDlg.inMieteGueltigBis.text())
            else:
                gueltigAb = QDate.fromString(tmp, "yyyy-MM-dd")

        retval = self.__showCalendar( gueltigBis )
        if type( retval ) == QDate:
            if senderName == 'tbMieteGueltigBis':
                self.__mieteDlg.inMieteGueltigBis.setText(retval.toString("yyyy-MM-dd"))
            else:
                self.__mieteDlg.inMieteGueltigBis_neu.setText(retval.toString("yyyy-MM-dd"))

    def __showCalendar(self, startDate ):
        cal = CalendarDlg(self)
        cal.calendar.setSelectedDate(startDate)
        retVal = cal.exec_()
        if retVal > 0:
            return QDate.fromJulianDay( retVal )
        else: return QVariant

    def resetDate(self, senderName: str):
        if senderName == 'tbResetMietGueltigAb':
            self.__mieteDlg.inMieteGueltigAb.setText('')
        elif senderName == 'tbResetMietGueltigBis':
            self.__mieteDlg.inMieteGueltigBis.setText('')
        elif senderName == 'tbResetMietGueltigAb_neu':
            self.__mieteDlg.inMieteGueltigAb_neu.setText('')
        elif senderName == 'tbResetMietGueltigBis_neu':
            self.__mieteDlg.inMieteGueltigBis_neu.setText('')

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

        if bindings.getWidgetValue('netto_miete', 'left') <= '0':
            return 'Netto-Miete darf nicht 0 sein.'

        if bindings.getWidgetValue('nk_abschlag', 'left') <= '0':
            return 'Nebenkosten-Abschlag darf nicht 0 sein.'

        gueltAb = bindings.getWidgetValue('gueltig_ab', 'left')
        if gueltAb == '':
            return 'Gültig ab darf nicht leer sein.'

        gueltAb = QDate.fromString( gueltAb, "yyyy-MM-dd" )
        if not gueltAb.isValid():
            return 'Gültig ab ist kein gültiges Datumsformat.'

        gueltBis = bindings.getWidgetValue('gueltig_bis', 'left')
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

        if bindings.getWidgetValue('netto_miete', 'right') <= '0':
            return 'Netto-Miete darf nicht 0 sein.'

        if bindings.getWidgetValue('nk_abschlag', 'right') <= '0':
            return 'Nebenkosten-Abschlag darf nicht 0 sein.'

        gueltAb = bindings.getWidgetValue('gueltig_ab', 'right')
        if gueltAb == '':
            return 'Gültig ab darf nicht leer sein.'

        gueltAb = QDate.fromString( gueltAb, "yyyy-MM-dd" )
        if not gueltAb.isValid():
            return 'Gültig ab ist kein gültiges Datumsformat.'

        gueltBisLeft = bindings.getWidgetValue('gueltig_bis', 'right')
        if gueltBisLeft <= '':
            return 'Werte auf der rechten Seite können erst eingetragen' \
                   'werden, wenn auf der linken Seite ein Gültig-bis-Datum ' \
                   'gesetzt wurde.'

        gueltBisLeft = QDate.fromString(gueltBisLeft, "yyyy-MM-dd")
        if gueltBisLeft > gueltAb:
            return 'Gültig bis auf der linken Seite ' \
                   'darf nicht größer sein als Gültig ab auf der rechten Seite.'

        gueltBis = bindings.getWidgetValue('gueltig_bis', 'right')
        if gueltBis > '':
            gueltBis = QDate.fromString( gueltBis, "yyyy-MM-dd" )
            if not gueltBis.isValid():
                return 'Gültig bis ist kein gültiges Datumsformat.'
            if not gueltBis > gueltAb:
                return 'Wenn Gültig bis angegeben ist, ' \
                       'muss es größer sein als Gültig ab.'

        return ''
