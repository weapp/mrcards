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
    
    def __get_bindings(self):
        if hasattr(self.core, "BindingManager"):
            return self.core.BindingManager
        else:
            r = self.main_app.find("#BindingManager")
            if r is None:
                raise Exception()
            else:
                return r
                
    bindings = property(__get_bindings)
    
    def bind(self, *args):
        self.bindings.bind(self, *args)
    
    def one(self, *args):
        self.bindings.one(self, *args)
    
    def trigger(self, *args):
        self.bindings.trigger(self, *args)
    
    def toggle(self, *args):
        self.bindings.toggle(self, *args)
    
    def unbind_(self, *args):
        self.bindings.unbind(self, *args)
        
    def new_event(self,event):
        return False
        
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