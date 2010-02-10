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

    def __setitem__(self, key, value):
        try: self.__del_child(key)
        except: pass
        sdwak.SDWAK.__setitem__(self,key,value)
        self.__add_child(key, value)
    
    def __delitem__(self, key):
        self.__del_child(key)
        sdwak.SDWAK.__delitem__(self, key)
    
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

    def append(self, value):
        if hasattr(value, 'id') and not value.id is None:
            key = value.id
            self[key] = value #no hace fallta  _add_child, se realiza en setitem
        else:
            key = sdwak.SDWAK.append(self, value)
            value.id = key
            self.__add_child(key, value)
        return key

    def actualize_childs(self):
        t = self.childs
        del self.childs[:]
        assert t is self.childs
        for key,value in self.iteritems():
            if (not hasattr(value, 'id')) or value.id is None:
                value.id = key
            self.add_child(value)
            
    def __add_child(self, key, value):
        if (not hasattr(value, 'id')) or value.id is None:
            value.id = key
        self.add_child(value)
    
    def __del_child(self, key):
        self.del_child(self[key])
    
    add=append
    
if __name__ == '__main__':
    pass
