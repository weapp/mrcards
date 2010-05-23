import pygame
from library.stdmodules import module
from library.stdmodules.apps import basicapp
from library.stdmodules.menu.menu2 import Menu as Menu2
from library.stdmodules.menu.menu import Menu
from library import core
import vbox

class menu(vbox.vbox):
	def __init__(self, parent):
		vbox.vbox.__init__(self, parent)
		
		#data
		self.position = 0
		self.menu_en_bucle = menu_en_bucle = True
		self.activate = activate = True
		self.persistant = persistant = True
		
		#appearance-data
		self.nvisibles = nvisibles = 6
		self.minvisible = 0
		self.maxvisible = nvisibles
		self.visible_options = self.get_childs()[self.minvisible:self.maxvisible]
		
		#eventos
		core.core.event.keydown['down'].bind(self.k_down)
		core.core.event.keydown['up'].bind(self.k_up)
		core.core.event.keydown['space'].bind(self.k_space)
		core.core.event.keydown['return'].bind(self.k_return)
		core.core.event.keydown['escape'].bind(self.k_escape)
	
	def add_child(self, option):
		vbox.vbox.add_child(self, option)
		self.visible_options = self.get_childs()[self.minvisible:self.maxvisible]
	
	def no_out(self, position):
		#actuacion en caso de que se salga del array
		if self.menu_en_bucle:
			position = position % len(self.get_childs())
		else:
			if position < 0:
				position = 0
			elif position >= len(self.get_childs()):
				position = len(self.get_childs())-1
		"""
		if self.position >= (self.maxvisible):
			self.minvisible = self.position-self.nvisibles+1
			self.maxvisible = self.position+1
			self.visible_options = self.get_childs()[self.minvisible:self.maxvisible]
			
		if self.position <= (self.minvisible):
			self.minvisible = self.position
			self.maxvisible = self.position+self.nvisibles
			self.visible_options = self.get_childs()[self.minvisible:self.maxvisible]
		"""
		return position
		
	def change_options(self,options):
		self.clear()
		for option in options:
			self.add_child(option)
		self.position = 0
		self.minvisible = 0
		self.maxvisible = self.nvisibles
		self.visible_options = self.get_childs()[self.minvisible:self.maxvisible]
		
	def down(self):
		self.item_on(self.position + 1)
		
	def up(self):
		self.item_on(self.position - 1)
	
	def item_on(self, position):
		self.get_childs()[self.position].hover_off()
		self.position = self.no_out(position)
		self.get_childs()[self.position].hover_on()
		
	def obtain_position(self):
		return self.position
		
	def k_escape(self, event, data):
		self.activate = not self.activate
		return True
	
	def k_return(self, event, data):
		if self.activate or self.persistant:
			self.get_childs()[self.position].select()
	
	def k_space(self, event, data):
		if self.activate or self.persistant:
			self.get_childs()[self.position].select()
					
	
	def k_up(self, event, data):
		if self.activate or self.persistant:
			self.up()
			
		
	def k_down(self, event, data):
		if self.activate or self.persistant:
			self.down()
		

	def seleccionar(self,n):
		pass