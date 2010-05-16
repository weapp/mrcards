#!/usr/bin/env python
#-*- coding:utf-8 -*-

#import xml.dom.minidom
from xml.dom import minidom
from xml.dom.minidom import Node
import time
"""
el parser ejecutaria una simulacion de:

#cabecera, siempre igual
import stateload as s
import core
c=core.core
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

VERBOSE = False

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
			
def cargar_estado(xmlfile, add, loader, children_allowed=True):
	for elem in parsear_estado(xmlfile, loader, children_allowed):
		add(elem)
		
def parsear_estado(xmlfile, loader, children_allowed=True):
	config = minidom.parse(xmlfile)
	state = config.firstChild
	assert state.tagName == "state"
	for obj in filter(lambda e:e.nodeType == Node.ELEMENT_NODE, state.childNodes):
		yield __parsear_objeto(obj, loader)

def attr(Node, attr):
	attr = Node.attributes.get(attr, None)
	return attr.value if not attr is None else None	


def __parsear_objeto(obj_node, loader, parent=None):
	t = time.clock()
	type_ = obj_node.tagName
	#type = obj_node.attributes["type"].value
	params = obj_node.attributes
	childs = []
	for node in filter(lambda e:e.nodeType == Node.ELEMENT_NODE, obj_node.childNodes):
		childs.append(node)
	constructor = getattr(loader, type_)
	
	#params = params.copy()
	i=params.items()
	params = {}
	for key, value in i:
		params[key] = value
	obj = constructor(parent,**params)
	for child in childs:
		obj.add_child( __parsear_objeto(child, loader, parent=obj))
	if VERBOSE: print "%5s %15s : %s" % (int((time.clock() - t)*10000), type(obj).__name__, obj.id )
	return obj
			

def first_nodeType(list, type):
	for obj in list:
		if obj.nodeType == type:
			return obj

'''
def __hasElementNodes(node):
	for elem in node.childNodes:
		if elem.nodeType == Node.ELEMENT_NODE:
			return True
	return False
	
def __hasCDATA(node):
	for elem in node.childNodes:
		if elem.nodeType == Node.CDATA_SECTION_NODE:
			return True
	return False
'''

if __name__ == "__main__": main()
