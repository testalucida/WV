#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Dict, Any, List
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtWidgets import QWidget, QTableView, QLineEdit, \
    QSpinBox, QCheckBox, QComboBox, QPlainTextEdit
#from ui import CalendarDlg
from business import DataProvider, ServiceError, WriteRetVal, AbstractWvException
from rechnungcontroller import RechnungController
from mietecontroller import MieteController
from hausgeldcontroller import HausgeldController
from models import WohnungenModel, WohnungItem, \
    RechnungenModel, Rechnung, RechnungItem, DictListTableModel, \
    DictTableRow, TableItem


class Controller():

    def __init__(self, mainWindow):
        self.__mainWindow = mainWindow
        self.__selectedWohnungItem = None
        self.__dataProvider = DataProvider()
        self.__rechnungController = None
        self.__mieteController = None
        self.__hausgeldController = None

    def initialize(self):
        self.__dataProvider.connect('martin', 'fuenf55') #TODO: login dialog
        self.__rechnungController = RechnungController( self.__dataProvider )
        self.__mieteController = MieteController(self.__dataProvider)
        self.__hausgeldController = HausgeldController(self.__dataProvider)

        resp = self.__dataProvider.getWohnungsUebersicht()
        whg_list = json.loads( resp.content )
        whg_model = WohnungenModel(whg_list)
        self.__mainWindow.tvWohnungen.setModel( whg_model)
        self.__mainWindow.tvWohnungen.expandAll()

    def onNewRechnungClicked(self) -> None:
        #item = self.__getSelectedWohnungTreeItem()
        if self.__selectedWohnungItem is not None:
            whg_short_ident = self.__getWohnungIdentifikation( self.__selectedWohnungItem.id())
            newRechnung = Rechnung()
            newRechnung.setValue('whg_id', self.__selectedWohnungItem.id())
            try:
                self.__rechnungController.newRechnung(whg_short_ident, newRechnung)
                self.__mainWindow.tblRechnungen.model().appendRow(newRechnung)
            except ServiceError as err:
                self.__mainWindow.showError(str(err.rc()), err.message())

    def onDeleteRechnungClicked(self) -> None:
        rechnungItem: TableItem = self.__getSelectedRechnungTableItem()
        if type(rechnungItem) == RechnungItem:
            rechnung = rechnungItem.rechnung()
            rg_id = rechnung.id()
            try:
                retval = self.__dataProvider.deleteRechnung(rg_id)
                self.__mainWindow.tblRechnungen.model().\
                    removeRow(rechnungItem.index().row())
            except ServiceError as err:
                self.__mainWindow.showError(str(err.message()['rc']),
                                            err.message()['msg'])


    '''
    a tree item has been selected.
    If this item is of type WohnungItem get data for all tabs
    '''
    def onWohnungenTreeClicked(self):
        self.__selectedWohnungItem = self.__getSelectedWohnungTreeItem()
        item = self.__selectedWohnungItem
        #self.__enableButtons( type( item ) == WohnungItem )
        if type( item ) == WohnungItem:
            #provide data for wohnung details:
            self.__provideDetails( item )
            #provide data for rechnungen:
            self.__provideRechnungen( item )
            #provide data for miete tab:
            self.__provideMieteData( item )
            #provide data for hausgeld tab
            self.__provideHausgeldData(item)
            # todo: provide data for other tabs:
            # 3. provide data for sonstige ein-/auszahlungen tab
            # 4. provide data for mieter tab
        else:
            self.__selectedWohnungItem = None
            self.__clearMainWindow()

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
                #rg_bezahlt_am = model.item(r, c).userData()['rg_bezahlt_am']
                rg_bezahlt_am = model.item(r, c).value('rg_bezahlt_am')
                if rg_bezahlt_am is not None and not rg_bezahlt_am.startswith(sel_item):
                    rows.append( r )
            self.__mainWindow.hideTableRechnungenRow( rows )

        except ValueError:

            return

    def onRechnungenTableDblClicked(self) -> None:
        """
        a row in tblRechnungen has been double clicked.
        Open the Rechnung dialog for browsing or editing
        :return: None
        """
        rechnungItem = self.__getSelectedRechnungTableItem()
        rechnung = rechnungItem.rechnung() #rechnung: list of RechnungItem

        #get Wohnung short identifikation:
        shortIdent = self.__getSelectedWohnungIdentifikation( )

        if self.__rechnungController.editRechnung(shortIdent, rechnung):
            #force rechnungen table to refresh:
            #rechnungen = self.__mainWindow.tblRechnungen.model()
            #rechnungen.changeRechnung(rg)
            pass

        return

    def onTestClicked(self):
        self.dumpRechnungenModel()

    def onMietenEdit(self) -> None:
        """
        a row in tblMieten has been double clicked or
        button "Miete anpassen..." has been clicked.
        Miete table could be empty.
        Open the Miete dialog for browsing or editing
        :return:
        """
        # get Wohnung short identifikation:
        shortIdent = self.__getSelectedWohnungIdentifikation()

        row: DictTableRow = self.__getBestRow(self.__mainWindow.tblMieten)
        if row is not None:
            tableItem = row.getItem('miete_id')
            rowAbove = self.__getRowAbove('miete_id', tableItem.value(),
                                          self.__mainWindow.tblMieten)
        else: #mietenTable is empty. row is still None
            #item = self.__getSelectedWohnungTreeItem()
            #item should always be of type WohnungsItem;
            #otherwise we wouldn't have a table to select in
            if self.__selectedWohnungItem is not None:
                whg_id = self.__selectedWohnungItem.id()

        try:
            if row is None:
                miete_row: DictTableRow = self.__mieteController.insertFirstMiete(whg_id, shortIdent)

                #model = self.__mainWindow.tblMieten.model()
                #model.setColumnNames(miete_row.columnNames())
                #model.appendRow(miete_row)
            else:
                self.__mieteController.editMiete(shortIdent, row, rowAbove)
        except AbstractWvException as e:
            self.__mainWindow.showError(
                "WvException in Controller.onMietenEdit:\n",
                                        e.toString())

        self.__provideMieteData(self.__selectedWohnungItem)

        return

    def __getBestRow(self, table: QTableView) -> DictTableRow:
        """
        returns either the selected row or in case no row is selected
        the top row
        :param table: QTableView to get the row from
        :return: the best row or None if table is empty
        """
        row: DictTableRow = self.__getSelectedRow(table)
        if row is None:
            row = self.__getTopRow(table)
        return row

    def onDeleteMiete(self):
        row: DictTableRow = self.__getSelectedRow(self.__mainWindow.tblMieten)
        if row is not None:
            mieteItem: TableItem = row.getItem('miete_id')
            try:
                self.__mieteController.deleteMiete(mieteItem.intValue())
                # self.__mainWindow.tblMieten.model(). \
                #     removeRow(mieteItem.index().row())
            except AbstractWvException as e:
                self.__mainWindow.showError(
                    "WvException in Controller.onDeleteMiete:\n",
                                            e.toString())
            self.__provideMieteData(self.__selectedWohnungItem)

    def onNewHausgeld(self):
        if self.__selectedWohnungItem is not None:
            # get Wohnung short identifikation:
            shortIdent = self.__getSelectedWohnungIdentifikation()
            whg_id = self.__selectedWohnungItem.id()
            row: DictTableRow = self.__hausgeldController.newHausgeld(whg_id, shortIdent)
            #read table data again:
            self.__provideHausgeldData(self.__selectedWohnungItem)
            #model = self.__mainWindow.tblHausgeld.model()
            #model.setColumnNames(row.columnNames())
            #model.appendRow(row)

    def onEditHausgeld(self):
        # get Wohnung short identifikation:
        shortIdent = self.__getSelectedWohnungIdentifikation()
        row: DictTableRow = self.__getBestRow(self.__mainWindow.tblHausgeld)
        if row is None:
            return

        self.__hausgeldController.editHausgeld(shortIdent, row)
        #read table data again:
        self.__provideHausgeldData(self.__selectedWohnungItem)

    def onDeleteHausgeld(self):
        row: DictTableRow = self.__getBestRow(self.__mainWindow.tblHausgeld)
        if row is None:
            return

        self.__hausgeldController.deleteHausgeld(row.getItem('hausgeld_id').value())
        #read table data again:
        self.__provideHausgeldData(self.__selectedWohnungItem)

    def dumpRechnungenModel(self):
        model = self.__mainWindow.tblRechnungen.model()
        rmax = model.rowCount()
        cmax = model.columnCount()
        for r in range(rmax):
            for c in range(cmax):
                val = model.data( model.index(r,c ) )
                print( r, '/', c, ': ', val )

    def __provideDetails(self, whg_item) -> None:
        """
        provides data for details tab
        :param whg_item:
        :return:
        """
        whg = self.__dataProvider.getWohnungDetails(whg_item.id())
        if 200 != whg.status_code:
            self.__mainWindow. \
                showError('Failed getting Wohnung details',
                          'status_code=' + str(whg.status_code) + '\n' +
                          whg.content.decode(encoding='UTF-8'))
            return
        details = json.loads(whg.content)
        self.__whgData2Ui(details)

    def __provideRechnungen(self, whg_item):
        """
        provides data for the rechnungen tab, that means
        all rechnungen for tblRechnungen and a distinct list of years
        to be used by the RechnungenFilter combobox
        :param whg_item:
        :return:
        """
        resp = self.__dataProvider.getRechnungsUebersicht( whg_item.id() )
        if 200 != resp.status_code:
            self.__mainWindow. \
                showError('Failed getting Rechnungsübersicht',
                          'status_code=' + str(resp.status_code) + '\n' +
                          resp.content.decode(encoding='UTF-8'))
            return
        rg_list = json.loads(resp.content)
        self.__rglistData2Ui(rg_list)

    def __provideMieteData(self, whg_item ):
        """
        provides data for the miete tab (both latest and former data)
        :param whg_item:
        :return:
        """
        resp = self.__dataProvider.getMieteData( whg_item.id() )
        miete_data = json.loads( resp.content )
        self.__mieteData2Ui( miete_data )

    def __provideHausgeldData(self, whg_item: WohnungItem) -> None:
        resp = self.__dataProvider.getHausgeldData(whg_item.id())
        hausgeld_data = json.loads(resp.content)
        self.__hausgeldData2Ui(hausgeld_data)

    def __getSelectedWohnungTreeItem(self) -> WohnungItem or None:
        """
        returns the selected tree item in tvWohnungen
        :return:
        """
        indexes = self.__mainWindow.tvWohnungen.selectedIndexes()
        if len(indexes) > 0:
            index = self.__mainWindow.tvWohnungen.selectedIndexes()[0]
            d = index.model().itemFromIndex(index)
            #print(d.data(Qt.DisplayRole))
            return d
        return None

    def __getSelectedRechnungTableItem(self):
        indexes = self.__mainWindow.tblRechnungen.selectedIndexes()
        if len(indexes) > 0:
            index = self.__mainWindow.tblRechnungen.selectedIndexes()[0]
            r = index.model().itemFromIndex(index) #r is of  type RechnungItem
            return r
        return QVariant

    '''
    returns the selectedRow of the given QTableView
    '''
    def __getSelectedRow(self, tableView) -> DictTableRow:
        indexes = self.__mainWindow.tblMieten.selectedIndexes()
        if len(indexes) > 0:
            index = indexes[0]
            selRow = index.model().itemFromIndex(index).dictTableRow()
            return selRow
        return None

    def __getTopRow(self, tableView: QTableView) -> DictTableRow:
        model = tableView.model()
        if model.rowCount() > 0:
            index = model.index(0,0)
            return model.itemFromIndex(index).dictTableRow()
        return None

    def __getRowAbove(self, key: str, value: str, tableView: QTableView) -> DictTableRow:
        index = self.__getIndexFrom(key, value, tableView)
        if index is None:
            #todo: raise exception
            return None

        model = tableView.model()
        if index.row() == 0:
            return None

        indexAbove = model.index(index.row()-1, 0)
        return model.itemFromIndex(indexAbove).dictTableRow()

    def __getIndexFrom(self, key: str, value: str, tableView: QTableView):
        model = tableView.model()
        rmax = model.rowCount()
        cmax = model.columnCount()
        for r in range(rmax):
            for c in range(cmax):
                item = model.item(r, c)
                if item.key() == key:
                    if item.value() == value:
                        index = model.indexFromItem(item)
                        r = index.row()
                        return index
        #todo: raise exception
        return None

    def __clearMainWindow(self):
        self.__clearMainWindow_(self.__mainWindow)

    def __clearMainWindow_(self, widget: QWidget) -> None:
        if isinstance(widget, QLineEdit):
            widget.clear()
        elif isinstance(widget, QSpinBox):
            widget.setValue(0)
        elif isinstance(widget, QPlainTextEdit):
            widget.setPlainText('')
        elif isinstance(widget, QCheckBox):
            widget.setChecked(False)
        elif isinstance(widget, QComboBox):
            widget.setCurrentIndex(0)
        elif isinstance(widget, QTableView):
            model = widget.model()
            model.clear()
        else:
            l = widget.children()
            for w in l:
                self.__clearMainWindow_(w)

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
        win = self.__mainWindow
        rechnungen = RechnungenModel( rg_list )
        win.tblRechnungen.setModel( rechnungen )
        win.tblRechnungen.resizeColumnsToContents()
        #hide rechnung id:
        win.tblRechnungen.setColumnHidden( 0, True )

        # TEST
        #self.dumpRechnungenModel()
        # TEST
        #provide distinct years for filter purposes:
        s = set()
        for rg in rg_list:
            #s.add(rg['rg_datum'][:4])
            if rg['rg_bezahlt_am'] is not None:
                s.add(rg['rg_bezahlt_am'][:4])
        s = sorted(s)
        l = []
        l.append( "Kein Jahresfilter" )
        for item in s:
            l.append( item )
        win.cboRechnungenFilter.clear()
        win.cboRechnungenFilter.addItems( l )

    def __mieteData2Ui(self, miete_data ):
        win = self.__mainWindow
        model = DictListTableModel(miete_data)
        win.tblMieten.setModel(model)
        #hide columns whg_id and miete_id:
        win.tblMieten.setColumnHidden(0, True)
        win.tblMieten.setColumnHidden(1, True)

    def __hausgeldData2Ui(self, hausgeld_data: List[Dict] ):
        win = self.__mainWindow
        model = DictListTableModel(hausgeld_data)
        win.tblHausgeld.setModel(model)
        #hide columns whg_id and miete_id:
        win.tblHausgeld.setColumnHidden(0, True)
        win.tblHausgeld.setColumnHidden(1, True)
        #win.tblHausgeld.setColumnWidth(2, 100)
        #win.tblHausgeld.setColumnWidth(3, 100)
        win.tblHausgeld.setColumnWidth(4, 150)
        win.tblHausgeld.setColumnWidth(5, 130)
        win.tblHausgeld.setColumnWidth(6, 130)

    def __getSelectedWohnungIdentifikation(self) -> str:
        #whg = self.__getSelectedWohnungTreeItem()
        if self.__selectedWohnungItem is not None:
            return self.__getWohnungIdentifikation(self.__selectedWohnungItem.id())

    def __getWohnungIdentifikation(self, whg_id) -> str:
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

