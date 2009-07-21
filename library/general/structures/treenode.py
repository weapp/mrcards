#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re

class TreeNode:
    def __init__(self,id=None,kind=None):
        self.id=id
        if kind is None:
            self.kind=[]
        else:
            self.kind=kind
        self.parent=None
        self.childs=[]

    def set_parent(self,parent):
        if not (self.parent is parent):
            try:
                self.parent.childs.remove(self)
            finally:
                self.parent=parent
                self.parent.add_child(self)

    def add_child(self,child):
        if not child in self.childs:
            self.childs.append(child)
            try: child.set_parent(self)
            except: pass
            
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
    
    def filter_objects(self, filter_,deep=True):
        childs=filter_by_isinstance(TreeNode,self.childs)
        r=filter_(childs)
        if deep:
            for obj in childs:
                r.extend(obj.filter_objects(filter_))
        return r
        
    def get_by_type(self,name):
        return self.filter_objects(filter_=filter_by_type(name))
        
    def get_by_kind(self,name):
        return self.filter_objects(filter_=filter_by_kind(name))
        
    def get_by_id(self,id):
        r=self.filter_objects(filter_=filter_by_id(id))
        return [r[0]] if r else []
        
    def get(self,expresion):
        expresion=expresion.split(' ')
        exp=expresion.pop(0)
        if exp==">": #comprueba que solo queramos de la primera capa de hijos, si es asi obtenemos la siguiente expresion
            exp=expresion.pop(0)
            resultados=self.filter_objects(filter_=filter_completo(exp), deep=False)
        else:
            resultados=self.filter_objects(filter_=filter_completo(exp))
            
        if expresion:
            r=[]
            for result in resultados:
                r.extend(result.get(' '.join(expresion)))
            resultados=r
        return resultados


def filter_by_isinstance(param, lista):
    def filter_(obj):
        return isinstance(obj,param)
    return filter(filter_,lista)

def filter_by_type(param):
    def filter__(lista):
        def filter_(obj):
            return obj.__class__.__name__==param
        return filter(filter_,lista)
    return filter__
    
def filter_by_id(param):
    def filter__(lista):
        def filter_(obj):
            return obj.id==param if hasattr(obj,'id') else False
        return filter(filter_,lista)
    return filter__

def filter_by_kind(param):
    def filter__(lista):
        def filter_(obj):
            return param in obj.kind if hasattr(obj,'kind') else False
        return filter(filter_,lista)
    return filter__
    
class filter_especial:
    def __init__(self,param):
        self.param=param
            
    def __call__(self,lista):
        if self.param=='even':
            r = [lista[i] for i in range(len(lista)) if ((i+1)%2)]
        elif self.param=='first' and lista:
            r = [lista[0]]
        elif self.param=='last' and lista:
            r = [lista[-1]]
        else:
            r = []
        return r
            

def filter_completo(param):
    def filter_(lista):
        for elem in re.findall(r'[#\.:]?[a-zA-Z0-9]*',param):
            if elem.startswith('#'):
                lista=filter_by_id(elem[1:])(lista)
            elif elem.startswith('.'):
                lista=filter_by_kind(elem[1:])(lista)
            elif elem.startswith(':'):
                lista=filter_especial(elem[1:])(lista)
            elif elem:
                lista=filter_by_type(elem)(lista)
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
    assert t.get('#prin')                           == []
    assert t.get('#a')                              == [a]
    assert t.get_by_id('a')                         == [a]
    assert t.get('#a #b')                           == [b]
    assert t.get('#a #c')                           == []
    assert t.get('#prin')                           == []
    assert t.get_by_kind('lalala')                  == t.get('.lalala')
    assert t.get('> TreeNode')                      == [a,c]
    assert t.get('> .lalala')                       == [c]
    assert t.get('.lalala > TreeNode')              == [e]
    assert t.get('.lalala')                         == [c, b]
    assert t.get('#c.lalala')                       == [c]
    assert t.get_by_type('TreeNode')                == t.get('TreeNode')
    assert t.get('TreeNode')                        == [a, c, b , e]
    assert t.get('TreeNode TreeNode TreeNode#e')    == [e]
    assert t.get('TreeNode:even')                   == [a, b, e]
    assert t.get('> TreeNode:first TreeNode')       == [b, e]
    assert t.get('TreeNode:last')                   == [c, b, e]
    
    raw_input("works")