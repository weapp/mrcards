#!/usr/bin/env python
#-*- coding:utf-8 -*-

import basicapp
from library.stdmodules import mvcmodule

class MVCApp(basicapp.BasicApp,mvcmodule.MVCModule):
    def __init__(self):
        mvcmodule.MVCModule.__init__(self,basicapp.BasicApp(),basicapp.BasicApp(),basicapp.BasicApp())
        basicapp.BasicApp.__init__(self)
    
    def new_event(self,event):
        mvcmodule.MVCModule.new_event(self,event)
        basicapp.BasicApp.new_event(self,event)
        
    def update(self):
        mvcmodule.MVCModule.update(self)
        basicapp.BasicApp.update(self)
   
    def draw(self):
        mvcmodule.MVCModule.draw(self)
        basicapp.BasicApp.draw(self)
