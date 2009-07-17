#!/usr/bin/env python
#-*- coding:utf-8 -*-

class TreeNode:
    def __init__(self,):
        self.parent=None
        self.childs=[]

    def set_parent(self,module):
        try:
            self.parent.remove(self)
        except:
            pass
        self.parent=module
        self.parent.childs.append(self)

    def add_child(self,child):
        try:
            child.set_parent(self)
        except:
            pass
			
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
