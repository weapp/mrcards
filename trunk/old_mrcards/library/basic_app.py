#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sortable_list

class Basic_app(sortable_list.Sortable_list):
    def new_event(self,event):        
        b=False
        self.reverse()
        for obj in self:
            if obj.new_event(event):
                b=True
                #print "evento[", repr(event.unicode) ,"]terminado por el objeto de tipo:", obj.__class___, ":",repr(objeto)
                break
        self.reverse()
        return b
    
    def update(self):
        map(lambda x: x.update(),self)
    
    def draw(self):
        """
        for obj in self:
            try:
                obj.draw()
            except:
                raise Exception("Draw method of " + repr(obj) + " is not avalible")
        """    
        map(lambda obj: obj.draw(),self)
        
    def updated(self):
        return True

