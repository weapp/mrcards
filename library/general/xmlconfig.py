#!/usr/bin/env python
#-*- coding:utf-8 -*-

import xml.dom.minidom

"""
el parser ejecutaria una simulacion de:

#cabecera, siempre igual
import stateload as s
import core
c=core.Core()
m=c.get_app().get_model()

#cuerpo
#lo que se nombra como objetos en el xml, simplemente pueden ser funciones que parseen de alguna manera los datos
#y que llamen a un constructor para que devuelvan un objeto

m.add(s.personaje(position=s.point(x="45",y="25"),name="Aaron",money="50"))
m.add(s.enemy(position=s.point("70","20"),ia="lala",destiny=s.point("20",y="45")))
m.add(s.place(----))


-------------modulo stateload--------------------------
#la funcion personaje podria ser algo asi:
def personaje(position,name,money):
    p=rpg.personaje(name)
    p.set_position(position)
    p.set_money(money)
    return p
    
def point(x=0,y=0):
    return ModuloNoseke.Vector2D(int(x),int(y))
"""

class stateload (object):
    """
    esta clase no es mas que para que no de error al ejecutar el codigo
    simula al modulo que contendra las funciones para cargar los objetos
    """
    def __init__(self):
        pass

    def __getattr__(self,attr):
        """
        simula las funciones que devolveran los objetos dentro del modulo.
        No tendrna por que ser necesariamente constructores.
        Los objetos que devuelven dichas funciones seran cadenas, que contienen
        el nombre y los parametros con que fue llamado.
        """
        def x (*args,**dic):
            return "<<"+attr + "("  + str(args) + str(dic) + ")"+">>"
        return x
        
    def add(self,attr):
        print "anyadiendo:"+attr
        
s=stateload()

def main():
    cargar_estado("./xml1.xml",s.add,s)
            
def cargar_estado(xmlfile,add,loader):
    config=xml.dom.minidom.parse(xmlfile)
    state=config.firstChild
    assert state.tagName == "state"
    for obj in state.childNodes:
        if obj.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
            add(__parsear_objeto(obj,loader))
    
def __parsear_objeto(obj,loader):
    assert obj.tagName == "obj"
    assert obj.attributes.has_key("type")
    args=[]
    dic={}
    for elem in obj.childNodes:
        if elem.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
            parametro=__parsear_parametro(elem,loader)
            if elem.attributes.has_key("name"):
                dic[str(elem.attributes.get("name").value)]=parametro
            else:
                args.append(parametro)
    constructor=getattr(loader,obj.attributes["type"].value) #aqui se utiliza s
    return constructor(*args,**dic)
            
def __parsear_parametro(elem,loader):
    assert elem.tagName == "param"
    if __hasElementNodes(elem):#si el parametro es un objeto,seguir profundizando
        for obj in elem.childNodes:
            if obj.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                return __parsear_objeto(obj,loader)
    else:
        return "".join(node.data for node in elem.childNodes).strip()

def __hasElementNodes(node):
    for elem in node.childNodes:
        if elem.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
            return True
    return False
	
def __hasCDATA(node):
    for elem in node.childNodes:
        if elem.nodeType == xml.dom.minidom.Node.CDATA_SECTION_NODE:
            return True
    return False

if __name__ == "__main__": main()
