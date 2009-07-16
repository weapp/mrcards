#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Sortable_list(list):
    def add(self,x):
        self.append(x)
        
    def top(self,x):
        self.append(self.pop(x))
        
    def bottom(self,x):
        self.insert(0,self.pop(x))
        
    def up(self,x):
        self.insert(x+1,self.pop(x))
        
    def down(self,x):
        if x>0:
            self.insert(x-1,self.pop(x))
