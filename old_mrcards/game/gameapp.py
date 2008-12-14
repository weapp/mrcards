#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library import mvcapp,basicapp
import rules
import gamezone

class GameApp(mvcapp.MVCApp):
    def __init__(self):
        mvcapp.MVCApp.__init__(self)
        
        
        self.m.update({'players': basicapp.BasicApp(), \
                            'deckdraws': basicapp.BasicApp(), \
                            'playzone': basicapp.BasicApp(), \
                            'deckdiscard': basicapp.BasicApp(), \
                            'deckpoints': basicapp.BasicApp()})
        self.m['rules']=rules.get_module('genericgame').Game()
        self.sub_app['gamezone']=gamezone.Gamezone(rules=self.m['rules'])
        
    def add(self,name,obj,kind='sub_app'):
        getattr(self,kind)[name]=obj
