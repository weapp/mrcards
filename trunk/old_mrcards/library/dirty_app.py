#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sortable_list

class Dirty_app(sortable_list.Sortable_list):
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
        updates=[]
        for obj in self:
            need_update=obj.update()
            if need_update and hasattr(need_update,'__iter__'):
                updates.extend(need_update)
        self.updates = filter(lambda x: type(x) is pygame.Rect, updates)
        return self.updates
    
    def draw(self):
        if self.updates:
            update=reduce(lambda x,y:pygame.Rect.union(x,y),self.updates)
            map(lambda obj:obj.draw(update),self)
