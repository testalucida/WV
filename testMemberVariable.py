#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Test:
    __mvar = 0

    def __init__(self):
        self.__mvar = 1
        __mvar = 2

    def showMvar(self):
        print( self.__mvar )


test = Test()
test.showMvar()