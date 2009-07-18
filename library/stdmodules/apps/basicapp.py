#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general.structures import tsdwak
from library.stdmodules import module

class BasicApp(tsdwak.TSDWAK,module.Module):
    def new_event(self,event):
        b=False
        self.reverse()
        for obj in self.values():
            if obj.new_event(event):
                b=True
                #print "evento[", repr(event.unicode) ,"]terminado por el objeto de tipo:", obj.__class___, ":",repr(objeto)
                break
        self.reverse()
        return b

    def update(self):
        map(lambda x: x.update(),self.values())

    def draw(self):
        """
        for obj in self.values():
            try:
                obj.draw()
            except:
                raise Exception("Draw method of " + repr(obj) + " is not avalible")
        """
        map(lambda obj:obj.draw(),self.values())

    def updated(self):
        return True