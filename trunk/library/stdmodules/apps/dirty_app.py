#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general.structures import sortablelist
import pygame

class Dirty_app(sortablelist.SortableList):
    def update(self):
        updates=[]
        for obj in self:
            need_update=obj.update()
            if need_update and hasattr(need_update,'__iter__'):
                updates.extend(need_update)
        self.updates = filter(lambda x: type(x) is pygame.Rect, updates)
        
    def updated(self):    
        return self.updates
    
    def draw(self):
        if self.updates:
            update=reduce(lambda x,y:pygame.Rect.union(x,y),self.updates)
            map(lambda obj:obj.draw(update),self)
