#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import requests
import json
from abc import ABC, abstractmethod

# def testRequests():
#     s = requests.Session() #create a persistent session
#     d = {
#         'user': 'martin',
#         'password': 'fuenf55'
#     }
#     r2 = s.post( 'http://localhost/kendelweb/dev/php/login.php', data=d )
#     if r2.status_code != 200:
#         return r2
#
#     #r = s.get( 'http://localhost/kendelweb/dev/php/business.php?q=uebersicht_wohnungen' )
#     d = {
#         'user': 'martin',
#         'q': 'uebersicht_wohnungen'
#     }
#     r = s.get('http://localhost/kendelweb/dev/php/business.php?q=uebersicht_wohnungen&user=martin' )
#     return r

class AbstractWvException(Exception):
    def __init__(self, rc: str, msg: str):
        Exception.__init__(self, rc, msg)
        self.__rc = rc
        self.__msg = msg

    def rc(self):
        return self.__rc

    def message(self):
        return self.__msg

    @abstractmethod
    def toString(self):
        pass

#+++++++++++++++++++++++++++++++++++++++++++++

class ServiceError(AbstractWvException):
    def __init__(self, rc, msg):
        AbstractWvException.__init__(self, rc, msg)

    def toString(self):
        return self.message()

#+++++++++++++++++++++++++++++++++++++++++++++

class DataError(AbstractWvException):
    def __init__(self, retVal: dict):
        AbstractWvException.__init__(self, retVal['rc'], retVal['errormsg'])
        self.__retVal = retVal

    def toString(self):
        s: str = '+++++DataError+++++\n'
        for k, v in self.__retVal.items():
            s = s + k + ': ' + str(v) + '\n'
        return s

#+++++++++++++++++++++++++++++++++++++++++++++

class ValidationError(AbstractWvException):
    def __init__(self, msg: str):
        AbstractWvException.__init__(self, '-1', msg)

    def toString(self):
        return self.message()

#+++++++++++++++++++++++++++++++++++++++++++++

class WriteRetVal:
    def __init__(self, rc, obj_id):
        self.__rc = rc
        self.__obj_id = obj_id
        #self.__msg = msg

    def rc(self):
        return self.__rc

    # def message(self):
    #     return self.__msg

    def object_id(self):
        return self.__obj_id

#+++++++++++++++++++++++++++++++++++++++++++++

class DataProvider:
    JSONERROR: int = -2

    def __init__(self ):
        self.__session = requests.Session()
        self.__user = ''

    def connect(self, user, pwd):
        self.__user = user
        d = {'user':user, 'password':pwd}
        resp = self.__session.post('http://localhost/kendelweb/dev/php/login.php', data=d )
        return resp

    def getWohnungsUebersicht(self):
        resp = self.__session.\
            get('http://localhost/kendelweb/dev/php/business.php?q=uebersicht_wohnungen&' +
                'user=' + self.__user)
        return resp

    def getWohnungDetails(self, whg_id ):
        resp = self.__session.\
            get('http://localhost/kendelweb/dev/php/business.php?q=detail&id=' + whg_id + '&user=' +
                self.__user )
        return resp

    def getWohnungIdentifikation(self, whg_id ):
        resp = self.__session.\
            get('http://localhost/kendelweb/dev/php/business.php?q=wohnung_kurz&id=' + whg_id + '&user=' +
                self.__user )
        return resp


    def getRechnungsUebersicht( self, whg_id ):
        resp = self.__session. \
            get('http://localhost/kendelweb/dev/php/business.php?q=uebersicht_rechnungen&id=' +
                str( whg_id ) + '&user=' + self.__user)
        return resp

    def getMieteData(self, whg_id ):
        resp = self.__session. \
            get('http://localhost/kendelweb/dev/php/business.php?q=miete_data&id=' +
                str(whg_id) + '&user=' + self.__user)
        return resp

    '''
    insert new Miete
    '''
    def insertMiete(self, miete: dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=insert_miete&user=' + self.__user,
                 data=miete)

        retval = self.__getWriteRetValOrRaiseException(resp)

        return retval

    def updateMiete(self, miete_dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=update_miete&user=' + self.__user, data=miete_dict)

        retval = self.__getWriteRetValOrRaiseException(resp)

        return retval

    def updateRechnung(self, rg_dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=update_rechnung&user=' + self.__user, data=rg_dict)

        retval = self.__getWriteRetValOrRaiseException(resp)

        return retval

    '''
    insert new rechnung
    '''
    def insertRechnung(self, rg_dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=insert_rechnung&user=' + self.__user, data=rg_dict)

        retval = self.__getWriteRetValOrRaiseException(resp)

        return retval

    '''
    delete rechnung
    '''
    def deleteRechnung(self, rg_id):
        delData = {}
        delData['rg_id'] = str(rg_id)
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=delete_rechnung&user=' + self.__user, data=delData)

        retval = self.__getWriteRetValOrRaiseException(resp)

        return retval

    def __getWriteRetValOrRaiseException(self, resp):
        if resp.status_code != 200:
            serviceError = ServiceError( resp.status_code, resp.text )
            print(serviceError.toString())
            raise serviceError

        dic = {}
        try:
            dic = json.loads(resp.content)
        except ValueError as e:
            msg: str = "+++++++++JSON Decode Error+++++++++\n" + e + \
                       "\nresp.content:\n" + resp.content + \
                       "\n+++++++++++++++++++++++++++++++++++\n"
            print(msg)
            raise ServiceError(self.JSONERROR, msg)

        if dic['rc'] != 0:
            dataError = DataError(dic)
            raise dataError

        return WriteRetVal(dic['rc'], dic['obj_id'])



######### For testing purposes only ########################

def getWohnungsUebersicht( ):
    f = urllib.request.urlopen('http://localhost/kendelweb/dev/php/business.php?q=uebersicht_wohnungen')
    js = f.read().decode( 'utf-8' )
    print(js)

    dec = json.loads( js ) #dec is a list now

    l = len(dec)
    print( "Länge: ", l )
    l = len( dec[1] )
    print( "Länge des zweiten Eintrags: ", l )
    print( dec[1] )
    print( dec[1]['ort'] )
    return dec



# r = testRequests()
# print( r.content )