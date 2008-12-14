#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sortabledict
import basicapp

class MVCApp(basicapp.BasicApp):
    def __init__(self):
        self.m = sortabledict.SortableDict()
        self.v = sortabledict.SortableDict()
        self.c = sortabledict.SortableDict()
        self.sub_app = sortabledict.SortableDict()

    def __new_event(self,event,dic):
        b = False
        items=dic.values()
        """for x in dic.items():
            if not (x is None):
                items.append(x)
        """
        items.reverse()
        
        for item in items:
            if item.new_event(event):
                b = True
                #print "evento[", repr(event.unicode) ,"]terminado por el objeto de tipo:", obj.__class___, ":",repr(objeto)
                continue
        return b

    def new_event(self,event):
        return self.__new_event(event,self.sub_app) and self.__new_event(event,self.c)

    def __update(self,dic):
        map(lambda x: x.update(),dic.itervalues())

    def update(self):
        #self.__update(self.m)
        self.__update(self.c)
        self.__update(self.sub_app)

    def __draw(self, dic):
        """
        for obj in self:
            try:
                obj.draw()
            except:
                raise Exception("Draw method of " + repr(obj) + " is not avalible")
        """
        map(lambda obj: obj.draw(),dic.itervalues())

    def draw(self):
        self.__draw(self.v)
        self.__draw(self.sub_app)

    def updated(self):
        return True
