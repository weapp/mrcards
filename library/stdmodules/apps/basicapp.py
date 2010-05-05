#!/usr/bin/env python
#-*- coding:utf-8 -*-
from library.general.structures import tsdwak
from library.stdmodules import module

class BasicApp(tsdwak.TSDWAK, module.Module):
    def __init__(self):
        module.Module.__init__(self)
        tsdwak.TSDWAK.__init__(self)

    def update(self):
        for x in self.values():
            x.update()

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