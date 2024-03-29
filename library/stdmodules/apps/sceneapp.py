#!/usr/bin/env python
#-*- coding:utf-8 -*-

import basicapp
from library import event

class SceneApp(basicapp.BasicApp):
    def __init__(self):
        self.onload = event.Event("onload")
        basicapp.BasicApp.__init__(self)
        self.__is_started = False
        
    def start_scene(self):
        self.onload()
        self.__is_started = True
        
    def end_scene(self):
        self.__is_started = False
        for elem in self.values():
            try:elem.unbind_()
            except:pass        
		
    def is_started():
        return self.__is_started
