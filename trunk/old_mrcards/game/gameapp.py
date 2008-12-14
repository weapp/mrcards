#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library import mvcapp,basicapp
import rules
import gamezone

class GameApp(mvcapp.MVCApp):
    def __init__(self):
        mvcapp.MVCApp.__init__(self)
        
        
        decks={'players': [], 'deckdraws': [], 'playzone': [], \
               'deckdiscard': [], 'deckpoints': []}
        self.m.update(decks)
        self.m['rules']=rules.get_module('genericgame').Game()
        self.sub_app['gamezone']=gamezone.Gamezone(rules=self.m['rules'])
        
    def add(self,name,obj,kind='sub_app'):
        getattr(self,kind)[name]=obj
