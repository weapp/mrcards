#!/usr/bin/env python
#-*- coding:utf-8 -*-
import module

class MVCModule (module.Module):
    def __init__(self,ModuleData=None,ModuleView=None,ModuleController=None):
        module.Module.__init__(self)
        self.m=ModuleData
        self.v=ModuleView
        self.c=ModuleController
        if not self.m is None:
            self.m.set_parent(self)
        if not self.v is None:
            self.v.set_parent(self)
        if not self.c is None:
            self.c.set_parent(self)
        
    def new_event(self,event):
        if not self.c is None:
            return self.c.new_event(event)

    def update(self):
        if not self.m is None:
            self.m.update()
        if not self.v is None:
            self.v.update()
        if not self.c is None:
            self.c.update()
        
    def draw(self):
        if not self.v is None:
            self.v.draw()
