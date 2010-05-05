#!/usr/bin/env python
#-*- coding:utf-8 -*-

#import xml.dom.minidom
from xml.dom import minidom
from xml.dom.minidom import Node
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
		yield __parsear_objeto(obj, loader, children_allowed)


class Params:
	def __init__(self):
		self.args = []
		self.dic = {}
		
	def add(self, key, value):
		if key is None:
			self.args.append(value)
		else:
			self.dic[str(key.value)] = value

def __parsear_objeto(obj, loader, children_allowed, parent=None):
	assert obj.tagName == "obj"
	assert obj.attributes.has_key("type")
	type = obj.attributes["type"].value
	params = Params()
	childs = []
	for node in filter(lambda e:e.nodeType == Node.ELEMENT_NODE, obj.childNodes):
		if node.tagName == "param":
			childnode = first_nodeType(node.childNodes, Node.ELEMENT_NODE)
			if not childnode is None:  #si el parametro es un objeto,seguir profundizando
				param = __parsear_objeto(childnode, loader, children_allowed)
			else:          #devolver la cadena
				param = "".join(node.data for node in node.childNodes).strip()
			params.add(node.attributes.get("name", None), param)
		elif node.tagName == "child" and children_allowed:
			childnode = first_nodeType(node.childNodes, Node.ELEMENT_NODE)
			assert not childnode is None
			childs.append(node)
		else: 
			assert (node.tagName == "param") or (node.tagName == "child" and children_allowed)
	constructor = getattr(loader, type)
	
	if parent is None:
		obj = constructor(*params.args,**params.dic)
	else:
		obj = constructor(parent, *params.args,**params.dic)
		
	for child in childs:
		child = first_nodeType(child.childNodes, Node.ELEMENT_NODE)
		child = __parsear_objeto(child, loader, children_allowed, parent=obj)
		#obj.add_child(child)
	
	
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
