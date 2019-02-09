#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QVariant, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QStandardItem, QStandardItemModel


class OrtItem( QStandardItem ):
    __plz = ''
    __ort = ''

    def __init__(self, plz, ort ):
        QStandardItem.__init__(self, plz + ' ' + ort)
        self.__plz = plz
        self.__ort = ort

    def plz_ort(self):
        return self.__plz  + ' ' + self.__ort

    def ort(self):
        return self.__ort


class StrasseItem( QStandardItem ):
    __str = ''

    def __init__(self, strasse ):
        QStandardItem.__init__(self, strasse)
        self.__str = strasse

    def strasse(self):
        return self.__str


class WohnungItem( QStandardItem ):
    __whg = None

    def __init__(self, whg ):
        QStandardItem.__init__(self, whg['whg_bez'])
        self.__whg = whg

    def test(self):
        return 'test'

    def id(self):
        return self.__whg['whg_id']

    def whg(self):
        return self.__whg


class WohnungenModel(QStandardItemModel):
    #__whg_list = None

    def __init__(self, whg_list):
        QStandardItemModel.__init__(self)
        self.__whg_list = whg_list

        # create structure like so:
        # 90429 Nürnberg
        #   Mendelstr. 24
        #       3.OG links
        #   Mendelstr. 24
        #       3. OG rechts
        # 91054 Erlangen
        #   Heuschlag 19
        #       Whg 23

        # for whg in whg_list: #iterating list
        #     for k, v in whg.items(): #iterating dictionary
        #         print( k, v )

        ort = None
        s = None

        for i, whg in enumerate( whg_list ):  # iterating list and increasing i

            if ort is None or ort.ort() != whg['ort']:
                ort = OrtItem( whg['plz'], whg['ort'] )
                self.setItem( i, ort )
                i += 1

            if s is None or s.strasse() != whg['strasse']:
                if s:
                    print( s.strasse(), '<-->', whg['strasse'] )
                    print( "left == right is ", s.strasse() == whg['strasse'] )
                s = StrasseItem( whg['strasse'] )
                ort.appendRow( s )

            wobez = WohnungItem( whg )
            s.appendRow( wobez )

        self.setHeaderData(0, Qt.Horizontal, "Alle Wohnungen")

    def data(self, idx, role=None):
        if role == Qt.DisplayRole:
            data = self.itemData(idx)
            return data[role]
        else:
            return QVariant()


class Rechnung(list): #list of RechnungItem
    #all rechnung data must be stored as list
    #due to its use in a QStandardItemModel
    def __init__(self, rg_dict = None):
        list.__init__(self)
        if rg_dict is not None:
            self.__rg_dict = rg_dict

        else: #create empty rechnung dictionary
            self.__rg_dict = {'whg_id': 0,
           'rg_id': '0',
           'rg_datum': '',
           'rg_nr': '',
           'betrag': '0',
           'verteilung_jahre': '1',
           'bemerkung': '',
           'firma': '',
           'rg_bezahlt_am': ''
           }

        for key, value in self.__rg_dict.items():
            item = RechnungItem(key, value)
            item.setRechnung(self)
            self.append(item)

        self.__id = self.__rg_dict['rg_id']

    def id(self):
        return self.__id

    def value(self, key):
        return self.__rg_dict[key]

    def setValue(self, key, newValue):
        #change __rg_dict - that's the master
        self.__rg_dict[key] = newValue
        #change corresponding RechnungItem in order to refresh
        #TableView
        for rechnungItem in self:
            if rechnungItem.key() == key:
                rechnungItem.setValue(newValue)

    def rechnungDictionary(self):
        return self.__rg_dict


class RechnungItem( QStandardItem ):
    #RechnungItem: one element of a Rechnung e.g. 'rg_datum'
    changed = pyqtSignal(str, str)

    def __init__(self, key, value ):
        QStandardItem.__init__(self, value )
        self.__key = key
        self.__value = value
        self.__rechnung = None

    def setValue(self, newVal):
        self.__value = newVal
        self.setData( newVal, Qt.EditRole)

    def value(self):
        return self.__value

    def key(self):
        return self.__key

    def setRechnung(self, rechnung):
        self.__rechnung = rechnung

    def rechnung(self):
        return self.__rechnung


class CustomItem( QStandardItem ):
    __userData = None

    def __init__(self, txt):
        QStandardItem.__init__( self, txt )
        if txt and txt.replace(".", "", 1).isdigit():
            self.setData(Qt.AlignRight | Qt.AlignVCenter, Qt.TextAlignmentRole)

    def setUserData(self, userData):
        self.__userData = userData

    def userData(self):
        return self.__userData


class RechnungenModel(QStandardItemModel):
    #__rg_list = None

    def __init__(self, rg_list):
        QStandardItemModel.__init__(self)
        self.__rg_list = rg_list
        #create a list of QStandardItems for each row
        for rg in rg_list:
            #headers = False;
            #row = []
            row = Rechnung(rg)

            #for key, value in rg.items():
                # if not headers:  ##this doesn't work if tableview contains only one row
                #     self.setHeaderData( i, Qt.Horizontal, key )
                #     i += 1
                #colVal = CustomItem( value )
                #colVal.setUserData( rg )
                #colVal = RechnungItem(key, value)
                #colVal.setRechnung(row)
                #row.append(colVal)

            self.appendRow(row)
            #headers = True

            i = 0
            for key, value in rg.items():
                self.setHeaderData(i, Qt.Horizontal, key)
                i += 1

    @pyqtSlot(str, str)
    def onChanged(self, key, val):
        print("changed!")

    def changeRechnung(self, rg):
        #find row - each row is a rechnung is a list entry
        rg_id = rg['rg_id']
        r = 0
        cmax = self.columnCount() - 1
        for row in self.__rg_list:
            if row['rg_id'] == rg_id:
                for c in range(cmax):
                    item = self.item(r, c)
                    idx = self.index(r, c)
                    self.setData(idx, 99.00)
            r += 1

    def columnId(self, colName):
        rg_dict = self.__rg_list[0]
        c = 0
        for key in rg_dict.keys():
            if key == colName:
                return c
            c += 1
        return -1  #todo: raise Error

    def value(self, row, col):
        return self.data( self.index(row, col) )

    def getRechnungen(self):
        return self.__rg_list