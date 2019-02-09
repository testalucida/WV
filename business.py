#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import requests
import json

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

class ServiceError(Exception):
    def __init__(self, rc, msg):
        Exception.__init__(self)
        self.__rc = rc
        self.__msg = msg

    def message(self):
        dic = {'rc': self.__rc, 'msg': self.__msg }
        return dic


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


class DataProvider:

    def __init__(self ):
        self.__session = requests.Session()

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

    def updateRechnung(self, rg_dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=update_rechnung&user=' + self.__user, data=rg_dict)

        retval = self.__getWriteRetVal(resp)
        if type(retval) == ServiceError:
            raise retval
        else:
            return retval

    '''
    insert new rechnung
    '''
    def insertRechnung(self, rg_dict):
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=insert_rechnung&user=' + self.__user, data=rg_dict)

        retval = self.__getWriteRetVal(resp)
        if type(retval) == ServiceError:
            raise retval
        else:
            return retval

    '''
    delete rechnung
    '''
    def deleteRechnung(self, rg_id):
        delData = {}
        delData['rg_id'] = str(rg_id)
        resp = self.__session. \
            post('http://localhost/kendelweb/dev/php/business.php?q=delete_rechnung&user=' + self.__user, data=delData)

        retval = self.__getWriteRetVal(resp)
        if type(retval) == ServiceError:
            raise retval
        else:
            return retval

    def __getWriteRetVal(self, resp):
        if resp.status_code != 200:
            serviceError = ServiceError( resp.status_code, resp.text )
            return serviceError
        else:
            dic = json.loads(resp.content)
            if dic['rc'] == 0:
                return WriteRetVal(dic['rc'], dic['obj_id'])
            else:
                serviceError = ServiceError(dic['rc'], resp.text)
                return serviceError


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