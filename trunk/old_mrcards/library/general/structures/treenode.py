#!/usr/bin/env python
#-*- coding:utf-8 -*-

class TreeNode:
    def __init__(self,):
        parent=None
        childs=[]

    def set_parent(self,module):
        parent=module
        
    """
    def add_parent(self,module):
        if not hasattr(self,'parents'):
            self.parents=[]
        elif not isinstance(self.parents,list):
            self.parents=[self.parents]
        self.parents.append(module)
    
    def remove_parent(self,module):
        self.parents.remove(module)
    """
