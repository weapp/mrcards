#!/usr/bin/env python
#-*- coding:utf-8 -*-

import UserList
import traceback

class Sortable_list(UserList.UserList):
    add = UserList.UserList.append
        
    def top(self, x):
        if -len(self) <= x < len(self):
            self.append(self.pop(x))
        else:
            traceback.extract_stack()
            raise IndexError("list index out of range")
        
    def bottom(self, x):
        if -len(self) <= x < len(self):
            self.insert(0, self.pop(x))
        else:
            traceback.extract_stack()
            raise IndexError("list index out of range")
        
    def up(self, x):
        if -len(self) <= x < len(self):
            self.insert(x+1, self.pop(x))
        else:
            traceback.extract_stack()
            raise IndexError("list index out of range")
        
    def down(self, x):
        if -len(self) <= x < len(self):
            self.insert(x-1, self.pop(x))
        else:
            traceback.extract_stack()
            raise IndexError("list index out of range")

			
#raw_input()