#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general.structures import treenode

class Module(treenode.TreeNode, object):
    #__metaclass__ = Meta_Verboso
    def __init__(self) :
        treenode.TreeNode.__init__(self)
        if type(self) is Module:
            raise AbstractClassException
        else:
            #constructor por defecto de las subclases
            from library import core
            self.core = core.core
            self._binds = {}
        
    def get_main_app(self):
        return self.core.get_app()
    
    main_app = property(get_main_app)
    
    def update(self):
        pass

    def draw(self):
        pass #not implemented now
        
    def _send_event(self,event):
        pass
    
    def _event_to_red(self,event):
        pass

    #def send_to_red(self,name,*args,**kw): #TODO mandar una funcion con el resultado
    
    #def get_from_red(self,name,*args,**kw): #TODO pedir al servidor el resultado de una funcion
    
    def event_to_red(self,name,*args,**kw):
        print "se esta ejecutando:", name, ", con los parametros:", args, kw
        getattr(self,name)(*args,**kw)
        
class AbstractClassException(Exception) :
    def __str__(self):
        return 'Esta clase es abstracta'