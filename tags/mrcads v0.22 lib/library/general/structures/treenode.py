#!/usr/bin/env python
#-*- coding:utf-8 -*-

        
class TreeNode:
    def __init__(self,):
        self.id=None
        self.kind=[]
        self.parent=None
        self.childs=[]

    def set_parent(self,module):
        try:
            self.parent.childs.remove(self)
        except:
            pass
        self.parent=module
        if not self in self.parent.childs:
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
    
    def filter_objects(self, filter=lambda x:True):
        r=[]
        for obj in self.childs:
            if isinstance(obj, TreeNode):
                if filter(obj):
                    r.append(obj)
                r.extend(obj.filter_objects(filter))
        return r
        
    def get_by_tagname(self,name):
        return self.filter_objects(filter=filter_by_tagname(name))
        
    def get_by_kind(self,name):
        return self.filter_objects(filter=filter_by_kind(name))
        
    def get_by_id(self,id):
        r=self.filter_objects(filter=filter_by_id(id))
        return [r[0]] if r else []
        
    def get(self,expresion):
        expr=expresion.split(' ')
        exp=expr[0]
        resultados=self.filter_objects(filter=filter_completo(exp))
        
        if len(expr)>1:
            r=[]
            for result in resultados:
                r.extend(result.get(' '.join(expr[1:])))
            resultados=r
        return resultados
    

class filter_by_id:
    def __init__(self, id):
        self.id=id
    def __call__(self, obj):
        if hasattr(obj,'id'):
            return obj.id==self.id
        else:
            return False

class filter_by_kind:
    def __init__(self, name):
        self.name=name
    def __call__(self, obj):
        if hasattr(obj,'kind'):
            return self.name in obj.kind
        else:
            return False

class filter_by_type:
    def __init__(self, name):
        self.name=name
    def __call__(self, obj):
        return type(obj).__name__==self.name

class filter_completo:
    def __init__(self,exp):
        dic=self.parsear_exp(exp)
        self.filters=[]
        if dic.has_key('type'):
            self.filters.append(filter_by_tagname(dic['type']))
        if dic.has_key('id'):
            self.filters.append(filter_by_id(dic['id']))
        if dic.has_key('kind'):
            self.filters.append(filter_by_kind(dic['kind']))
    
    def __call__(self,obj):
        r=True
        for filter in self.filters:
            r &= filter(obj)
        return r

    def parsear_exp(self,exp):
        pnt=exp.find('.')
        shr=exp.find('#')
        if exp.startswith('#'):
            if pnt!=-1:
                r={'id':exp[1:pnt]}
                r['kind']=self.parsear_exp(exp[pnt:])['kind']
            else:
                r={'id':exp[1:]}
        elif exp.startswith('.'):
            if shr!=-1:
                r={'kind':exp[1:shr]}
                r['id']=self.parsear_exp(exp[shr:])['id']
            else:
                r={'kind':exp[1:]}
        else:
            if max(shr, pnt)==-1:#no tiene # ni .
                r={'type':exp}
            else:#tiene al menos # o .
                if min(shr, pnt)!=-1:#tiene # y .
                    r={'tag':exp[:min(shr, pnt)]}
                    r.update(self.parsear_exp(exp[min(shr, pnt):]))
                else: #solo tiene uno de los dos
                    r={'tag':exp[:max(shr, pnt)]}
                    r.update(self.parsear_exp(exp[max(shr, pnt):]))
        return r