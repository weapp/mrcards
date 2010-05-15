#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
from library.general import singleton
import random

class Ids:
    __metaclass__ = singleton.Singleton
    def __init__(self):
        self.ids = {}
    def generate_valid_id(self):
        id = None
        keys = self.ids.keys()
        while (id is None) or (id in keys):
            id = random.randint(3,100)
        return id
ids = Ids()
    
class TreeNode:
    def __init__(self, id=None, kind=None):
        self.id = id
        self.key = id
        if kind is None:
            self.kind = []
        else:
            self.kind = kind
        self.parent = None
        self.__childs = {}

    def get_id(self):
        return self.__id
        
    def set_id(self, id):
        self.__id = id if not id is None else ids.generate_valid_id()

    id = property(get_id, set_id)
    
    def clear(self):
        self.__childs.clear()
    
    def set_parent(self, parent):
        if not (self.parent is parent):
            if hasattr(self.parent, "del_child"):
                self.parent.del_child(self, None)
            self.parent = parent

    def add_child(self, child, key=0):
        if not child in self.__childs.setdefault(key, []):
            self.__childs[key].append(child)
            if hasattr(child, "set_parent"):
                child.set_parent(self)
    
    def get_childs(self, key=0):
        return self.__childs.get(key,[])[:]
    
    def del_child(self, child, key=0):
        self.__childs.get(key,[]).remove(child)
        
    def get_all_childs(self):
        r = []
        for childs in self.__childs.values():
            r.extend(childs)
        return r
        
    """
    def add_parent(self, module):
        if not hasattr(self, 'parents'):
            self.parents = []
        elif not isinstance(self.parents, list):
            self.parents = [self.parents]
        self.parents.append(module)
    
    def remove_parent(self,module):
        self.parents.remove(module)
    """
    
    def filter_objects(self, filter_, deep=True):
        childs = filter_by_isinstance(TreeNode, self.get_all_childs())
        r = filter_(childs)
        if deep:
            for obj in childs:
                r.extend(obj.filter_objects(filter_))
        return r
        
    def search_by_type(self, name):
        return self.filter_objects(filter_=filter_by_type(name))
        
    def search_by_kind(self, name):
        return self.filter_objects(filter_=filter_by_kind(name))
        
    def search_by_id(self, id):
        r=self.filter_objects(filter_=filter_by_id(id))
        return [r[0]] if r else []
		
    def search_by_key(self, key):
        r=self.filter_objects(filter_=filter_by_key(key))
        return [r[0]] if r else []
        
    def __search(self, expresion='> *'):
        expresion=expresion.split(' ')
        exp=expresion.pop(0)
        if exp == ">": #comprueba que solo queramos de la primera capa de hijos, si es asi obtenemos la siguiente expresion
            exp = expresion.pop(0)
            resultados = self.filter_objects(filter_=filter_completo(exp), deep=False)
        else:
            resultados = self.filter_objects(filter_ = filter_completo(exp))
            
        if expresion:
            r = []
            for result in resultados:
                r.extend(result.__search(' '.join(expresion)))
            resultados = r
        return resultados
        
    def search(self,*args,**kws):
        list_=self.__search(*args,**kws)
        nodup=[]
        for elem in list_:
            if elem not in nodup:
                nodup.append(elem)
        return nodup
        
    def find(self, *args, **kws):
        r = self.search(*args, **kws)
        if len(r):
            return r[0]

def filter_by_isinstance(param, lista):
    def filter_(obj):
        return isinstance(obj,param)
    return filter(filter_,lista)

def filter_by_type(param):
    def filter__(lista):
        def filter_(obj):
            return obj.__class__.__name__==param
        return filter(filter_, lista)
    return filter__
    
def filter_by_id(param):
    def filter__(lista):
        def filter_(obj):
            return obj.id == param if hasattr(obj,'id') else False
        return filter(filter_,lista)
    return filter__

def filter_by_key(param):
    def filter__(lista):
        def filter_(obj):
            return obj.key == param if hasattr(obj,'key') else False
        return filter(filter_,lista)
    return filter__

def filter_by_kind(param):
    def filter__(lista):
        def filter_(obj):
            return param in obj.kind if hasattr(obj,'kind') else False
        return filter(filter_, lista)
    return filter__
    
class filter_especial:
    def __init__(self, param):
        self.param=param
            
    def __call__(self, lista):
        if self.param == 'even':
            r = [lista[i] for i in range(len(lista)) if ((i+1)%2)]
        elif self.param == 'first' and lista:
            r = [lista[0]]
        elif self.param == 'last' and lista:
            r = [lista[-1]]
        else:
            r = []
        return r

def filter_completo(param):
    def filter_(lista):
        if param == "*":
            return lista
        for elem in re.findall(r'[#&\.%]?[a-zA-Z0-9]*',param):
            if elem.startswith('#'):
                lista = filter_by_id(elem[1:])(lista)
            elif elem.startswith('&'):
                lista = filter_by_key(elem[1:])(lista)
            elif elem.startswith('.'):
                lista = filter_by_kind(elem[1:])(lista)
            elif elem.startswith('%'):
                lista = filter_especial(elem[1:])(lista)
            elif elem:
                lista = filter_by_type(elem)(lista)
        return lista
    return filter_


if __name__ == "__main__":
    t=TreeNode('prin')
    a=TreeNode('a')
    b=TreeNode('b',['lalala'])
    c=TreeNode('c',['lalala'])
    d=TreeNode('d')
    e=TreeNode('e')
    
    t.add_child(a)
    t.add_child(c)
    a.add_child(b)
    b.add_child(e)
    
    """
    t
        a
            b
                e
        c
    """
    assert t.search()                                  == t.get_childs()
    assert t.search('#prin')                           == []
    assert t.search('#a')                              == [a]
    assert t.search_by_id('a')                         == [a]
    assert t.search('#a #b')                           == [b]
    assert t.search('#a #c')                           == []
    assert t.search('#prin')                           == []
    assert t.search_by_kind('lalala')                  == t.search('.lalala')
    assert t.search('> TreeNode')                      == [a,c]
    assert t.search('> .lalala')                       == [c]
    assert t.search('.lalala > TreeNode')              == [e]
    assert t.search('.lalala')                         == [c, b]
    assert t.search('#c.lalala')                       == [c]
    assert t.search_by_type('TreeNode')                == t.search('TreeNode')
    assert t.search('TreeNode')                        == [a, c, b , e]
    assert t.search('TreeNode TreeNode TreeNode#e')    == [e]
    assert t.search('TreeNode:even')                   == [a, b, e]
    assert t.search('> TreeNode:first TreeNode')       == [b, e]
    assert t.search('TreeNode:last')                   == [c, b, e]
    
    raw_input("works")