#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sdwak
import treenode

class TSDWAK(sdwak.SDWAK, treenode.TreeNode):
    """
    Tree Sortable Dict With Autokeys
    """
    def __init__(self):
        sdwak.SDWAK.__init__(self)
        treenode.TreeNode.__init__(self)

    def __setitem__(self,key,value):
        sdwak.SDWAK.__setitem__(self,key,value)
        self.actualize_childs()
    
    def __delitem__(self,x):
        sdwak.SDWAK.__delitem__(self,x)
        self.actualize_childs()
	
    def clear(self):
        sdwak.SDWAK.clear(self)
        self.actualize_childs()

    def pop(self,x):
        sdwak.SDWAK.pop(self,x)
        self.actualize_childs()

    def popitem(self):
        sdwak.SDWAK.popitem(self)
        self.actualize_childs()

    def update(self,*args,**kw):
        sdwak.SDWAK.update(self,*args,**kw)
        self.actualize_childs()

    def append(self,x):
        sdwak.SDWAK.append(self,x)
        treenode.TreeNode.add_child(self,x)

    def actualize_childs(self):
        self.childs=[]
        map(self.add_child, self.itervalues())

    add=append
    
if __name__ == '__main__':
    pass
