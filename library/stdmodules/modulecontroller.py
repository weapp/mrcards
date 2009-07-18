#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general.structures import treenode

class ModuleController (treenode.TreeNode):

    def __init__(self):
        treenode.TreeNode.__init__(self)
        pass

    def update(self):
        pass
        
    def new_event(self):
        pass
        
    def _send_event(self,event):
        pass
    
    def _event_to_red(self,event):
        pass

    #def send_to_red(self,name,*args,**kw): #TODO mandar una funcion con el resultado
    
    #def get_from_red(self,name,*args,**kw): #TODO pedir al servidor el resultado de una funcion
    
    def event_to_red(self,name,*args,**kw):
        print "se esta ejecutando:", name, ", con los parametros:", args, kw
        getattr(self,name)(*args,**kw)
    
