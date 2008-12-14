#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library import mvcapp,basicapp
import rules
import gamezone

class GameApp(mvcapp.MVCApp):
    def __init__(self):
        mvcapp.MVCApp.__init__(self)
        
        
        self.sub_app.update({'players': basicapp.BasicApp(), \
                            'deckdraws': basicapp.BasicApp(), \
                            'playzone': basicapp.BasicApp(), \
                            'deckdiscard': basicapp.BasicApp(), \
                            'deckpoints': basicapp.BasicApp()})
        self.m['rules']=rules.get_module('genericgame').Game()
        self.sub_app['gamezone']=gamezone.Gamezone(rules=self.m['rules'])
