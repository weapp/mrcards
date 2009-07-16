#!/usr/bin/env python
#-*- coding:utf-8 -*-

class SortableList(list):
    add = list.append
        
    def top(self, x):
        self.append(self.pop(x))
        
    def bottom(self, x):
        self.insert(0, self.pop(x))
        
    def up(self, x):
        self.insert(x + 1, self.pop(x))
        
    def down(self, x):
        if x>0:
            self.insert(x - 1, self.pop(x))

    def top_elem(self, x):
        self.append(self.pop(self.index(x)))
        
    def bottom_elem(self, x):
        self.insert(0, self.pop(self.index(x)))
        
    def up_elem(self, x):
        index = self.index(x)
        self.insert(index + 1, self.pop(index))
        
    def down_elem(self, x):
        if x > 0:
            index = self.index(x)
            self.insert(index - 1,self.pop(index))
