#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import copy
from numbers import Number
from PyQt5.QtCore import Qt, QVariant, QDate
from ui import WvDialog, CalendarDlg
from business import DataProvider, ServiceError
from models import DictTableRow
from bindings import *

class MieteController:

    def __init__(self, dataProvider):
        self.__dataProvider = dataProvider
        self.__mieteDlg = None

    def editMiete(self, whg_short,
                  miete: DictTableRow,
                  mieteNewer: DictTableRow = None):
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

        self.__mieteDlg = WvDialog("miete31.ui")
        dlg = self.__mieteDlg
        dlg.setWohnungIdent(whg_short)
        # check Gueltig_bis: if in the past, enable just bemerkung
        # gueltig_bis = miete.value('gueltig_bis')
        # if gueltig_bis > ' ':
        #     bisDate = QDate.fromString( gueltig_bis, "yyyy-MM-dd" )
        #     today = QDate.currentDate()

        self.__bind(dlg, miete, mieteNewer)

        if dlg.exec_() > 0:
            if mieteNewer.value('miete_id') == '' and \
                    mieteNewer.value('netto_miete') > '':
                try:
                    self.__dataProvider.insertMiete(mieteNewer.dictionary())
                except:
                    import sys
                    e = sys.exc_info()[0]
                    print("Insert Miete: " + e)
            #resp = self.__dataProvider.updateMiete( ??? )
            #dic = json.loads(resp.content)
            #if dic['rc'] == 0:
            #    return True
            pass
        return False

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

    def __bind(self, dlg: WvDialog,
               miete: DictTableRow,
               mieteNeu: DictTableRow):
        bs = Bindings()
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

    def validate(self):
        val = self.__mieteDlg.value("inNettoMiete")
        return True