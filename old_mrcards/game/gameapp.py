#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.stdmodules.apps import mvcapp,basicapp
import rules
import gamezone

class GameApp(mvcapp.MVCApp):
    def __init__(self):
        mvcapp.MVCApp.__init__(self)
        
        
        decks={'players': basicapp.BasicApp(), 'deckdraws': basicapp.BasicApp(), 'playzone': basicapp.BasicApp(), \
               'deckdiscard': basicapp.BasicApp(), 'deckpoints': basicapp.BasicApp()}
        self.m.update_items(decks)
        self.m['rules']=rules.get_module('genericgame').Game()
        self['gamezone']=gamezone.Gamezone(rules=self.m['rules'])
        
    def add(self,name,obj,kind='sub_app'):
        if kind=='sub_app':
            self[name]=obj
        else:
            getattr(self,kind)[name]=obj
