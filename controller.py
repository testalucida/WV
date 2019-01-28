#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from PyQt5.QtCore import Qt, QVariant
#from PyQt5.QtWidgets import  QAbstractItemView
#from ui import CalendarDlg
from business import DataProvider
from rechnungcontroller import RechnungController
from models import WohnungenModel, WohnungItem, RechnungenModel


class Controller():
    __dataProvider = None
    __mainWindow = None
    __rechnungController = None
    #__rechnungDlg = None

    def __init__(self, mainWindow):
        self.__mainWindow = mainWindow
        self.__dataProvider = DataProvider()

    def initialize(self):
        self.__dataProvider.connect('martin', 'fuenf55') #TODO: login dialog
        self.__rechnungController = RechnungController( self.__dataProvider )
        resp = self.__dataProvider.getWohnungsUebersicht()
        whg_list = json.loads( resp.content )
        whg_model = WohnungenModel(whg_list)
        self.__mainWindow.tvWohnungen.setModel( whg_model)
        self.__mainWindow.tvWohnungen.expandAll()

    def onNewRechnungClicked(self):
        item = self.__getSelectedWohnungTreeItem()
        if type( item ) == WohnungItem:
            self.__rechnungController.newRechnung()

    '''
    onFilterRechnungenClicked: extract a list out of the years of 
    the rechnung dates and use it for a filter dialog.
    hide all rows in tblRechnungen not satisfying the selected 
    year criterium 
    '''
    # def onFilterRechnungenClicked(self):
    #     rg_list = self.__mainWindow.tblRechnungen.model().getRechnungen()
    #     s = set()
    #     for rg in rg_list:
    #         s.add(rg['rg_datum'][:4])
    #
    #     s = sorted(s)
    #
    #
    #     return

    '''
    a tree item has been selected.
    If this item is of type WohnungItem get data for all tabs
    '''
    def onWohnungenTreeClicked(self):
        item = self.__getSelectedWohnungTreeItem()
        #self.__enableButtons( type( item ) == WohnungItem )
        if type( item ) == WohnungItem:
            self.__provideDetails( item )
            self.__provideRechnungen( item )

    '''
    on Rechnungen tab a year filter was set.
    check which one and hide rows not matching the
    year criterium
    '''
    def onRechnungenFilterChanged(self):
        self.__mainWindow.clearFilter()
        sel_item = self.__mainWindow.cboRechnungenFilter.currentText()
        try:
            year = int(sel_item)
            model = self.__mainWindow.tblRechnungen.model()
            rmax = model.rowCount()
            #get index of rg_datum column
            ##c = model.columnId('rg_datum')
            c = model.columnId('rg_bezahlt_am')
            #iterate over all rows and check dates in column 'rg_datum'
            rows = []
            for r in range(rmax):
                #rg_datum = model.item(r,c).userData()['rg_datum']
                rg_bezahlt_am = model.item(r, c).userData()['rg_bezahlt_am']
                #if not rg_datum.startswith( sel_item ):
                if rg_bezahlt_am is not None and not rg_bezahlt_am.startswith(sel_item):
                    rows.append( r )
            self.__mainWindow.hideTableRechnungenRow( rows )

        except ValueError:

            return



    '''
    a row in tblRechnungen has been double clicked. 
    Open the Rechnung dialog for browsing or editing
    '''
    def onRechnungenTableDblClicked(self):
        r = self.__getSelectedRechnungTableItem()
        rg = r.userData()
        #get Wohnung short identifikation:
        whg = self.__getSelectedWohnungTreeItem()
        shortIdent = self.__getWohnungIdentifikation( whg.id() )

        self.__rechnungController.editRechnung(shortIdent, rg)
        return

    def onTestClicked(self):
        self.dumpRechnungenModel()

    def dumpRechnungenModel(self):
        model = self.__mainWindow.tblRechnungen.model()
        rmax = model.rowCount()
        cmax = model.columnCount()
        for r in range(rmax):
            for c in range(cmax):
                val = model.data( model.index(r,c ) )
                print( r, '/', c, ': ', val )

    '''
    provides data for the details tab
    '''
    def __provideDetails(self, whg_item):
        whg = self.__dataProvider.getWohnungDetails(whg_item.id())
        if 200 != whg.status_code:
            self.__mainWindow. \
                showError('Failed getting Wohnung details',
                          'status_code=' + str(whg.status_code) + '\n' +
                          whg.content.decode(encoding='UTF-8'))
            return
        details = json.loads(whg.content)
        self.__whgData2Ui(details)

    '''
    provides data for the rechnungen tab, that means 
    all rechnungen for tblRechnungen and a distinct list of years 
    to be used by the RechnungenFilter combobox
    '''
    def __provideRechnungen(self, whg_item):
        resp = self.__dataProvider.getRechnungsUebersicht( whg_item.id() )
        if 200 != resp.status_code:
            self.__mainWindow. \
                showError('Failed getting Rechnungsübersicht',
                          'status_code=' + str(resp.status_code) + '\n' +
                          resp.content.decode(encoding='UTF-8'))
            return
        rg_list = json.loads(resp.content)
        self.__rglistData2Ui(rg_list)

    '''
    returns the selected tree item in tvWohnungen
    '''
    def __getSelectedWohnungTreeItem(self):
        indexes = self.__mainWindow.tvWohnungen.selectedIndexes()
        if len(indexes) > 0:
            index = self.__mainWindow.tvWohnungen.selectedIndexes()[0]
            d = index.model().itemFromIndex(index)
            #print(d.data(Qt.DisplayRole))
            return d
        return QVariant

    def __getSelectedRechnungTableItem(self):
        indexes = self.__mainWindow.tblRechnungen.selectedIndexes()
        if len(indexes) > 0:
            index = self.__mainWindow.tblRechnungen.selectedIndexes()[0]
            r = index.model().itemFromIndex(index)
            return r
        return QVariant

    def __whgData2Ui(self, details ):
        self.__mainWindow.inPlz.setText( details['plz'] )
        self.__mainWindow.inOrt.setText(details['ort'])
        self.__mainWindow.inStrasse.setText(details['strasse'])
        self.__mainWindow.inWhgBez.setText(details['whg_bez'])
        self.__mainWindow.spinZimmer.setValue(int( details['zimmer'] ) )
        self.__mainWindow.inQm.setText(details['qm'])
        cbo = self.__mainWindow.cboBalkon
        #allItems = [cbo.itemText(i) for i in range(cbo.count())]
        index = cbo.findText( details['balkon'], Qt.MatchFixedString )
        if index >= 0:
            cbo.setCurrentIndex(index)

        checked = details['ebk'] == 'J'
        self.__mainWindow.cbEbk.setChecked( checked )

        cbo = self.__mainWindow.cboHeizung
        index = cbo.findText( details['heizung'], Qt.MatchFixedString )
        if index >= 0:
            cbo.setCurrentIndex(index)

        self.__mainWindow.txtZusatz.setPlainText( details['zusatz'] )

        checked = details['tageslichtbad'] == 'J'
        self.__mainWindow.cbTageslicht.setChecked(checked)

        checked = details['dusche'] == 'J'
        self.__mainWindow.cbDusche.setChecked(checked)

        checked = details['badewanne'] == 'J'
        self.__mainWindow.cbWanne.setChecked(checked)

        checked = details['bidet'] == 'J'
        self.__mainWindow.cbBidet.setChecked(checked)

        checked = details['kellerabteil'] == 'J'
        self.__mainWindow.cbKeller.setChecked(checked)

        checked = details['aufzug'] == 'J'
        self.__mainWindow.cbAufzug.setChecked(checked)

        cbo = self.__mainWindow.cboGarage
        index = cbo.findText(details['garage'], Qt.MatchFixedString)
        if index >= 0:
            cbo.setCurrentIndex(index)

        self.__mainWindow.txtBemerk.setPlainText(details['bemerkung'])

    def __rglistData2Ui(self, rg_list ):
        rechnungen = RechnungenModel( rg_list )
        self.__mainWindow.tblRechnungen.setModel( rechnungen )
        self.__mainWindow.tblRechnungen.resizeColumnsToContents()
        #hide rechnung id:
        self.__mainWindow.tblRechnungen.setColumnHidden( 0, True )

        # TEST
        self.dumpRechnungenModel()
        # TEST
        #provide distinct years for filter purposes:
        s = set()
        for rg in rg_list:
            #s.add(rg['rg_datum'][:4])
            if rg['rg_bezahlt_am'] is not None:
                s.add(rg['rg_bezahlt_am'][:4])
        s = sorted(s)
        l = [];
        l.append( "Kein Jahresfilter" )
        for item in s:
            l.append( item )
        self.__mainWindow.cboRechnungenFilter.clear()
        self.__mainWindow.cboRechnungenFilter.addItems( l )

    def __getWohnungIdentifikation(self, whg_id):
        resp = self.__dataProvider.getWohnungIdentifikation(whg_id)
        if 200 != resp.status_code:
            self.__mainWindow. \
                showError('Failed getting Wohnung details',
                          'status_code=' + str(resp.status_code) + '\n' +
                          resp.content.decode(encoding='UTF-8'))
            return
        dict = json.loads(resp.content)

        line1 = dict.get( 'plz' )
        line1 += ' '
        line1 += dict.get( 'ort' )

        line2 = dict.get( 'strasse' )
        line2 += ' / '
        line2 += dict.get( 'whg_bez' )

        ident = '<html><head/><body><p><span style=" font-weight:600; color:#204a87;">'
        ident += line1
        ident +='<br>'
        ident += line2
        ident += '</span></p></body></html>'

        return ident

