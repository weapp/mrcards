import pygame
from library.stdmodules import module
from library.stdmodules.apps import basicapp
from library.stdmodules.menu.menu2 import Menu as Menu2
from library.stdmodules.menu.menu import Menu
from library import core

class menu(basicapp.BasicApp):
	def __init__(self, pos):
		basicapp.BasicApp.__init__(self)
		
		#data
		self.options = []
		self.position = 0
		self.menu_en_bucle = menu_en_bucle = True
		self.activate = activate = True
		self.persistant = persistant = True
		self.i = 0
		
		#appearance-data
		self.nvisibles = nvisibles = 6
		self.minvisible = 0
		self.maxvisible = nvisibles
		self.visible_options = self.options[self.minvisible:self.maxvisible]
		
		#appearance
		self.pos = pos
		self.g = pygame.sprite.Group()
		
		
		#eventos
		core.core.event.keydown['down'].bind(self.k_down)
		core.core.event.keydown['up'].bind(self.k_up)
		core.core.event.keydown['space'].bind(self.k_space)
		core.core.event.keydown['return'].bind(self.k_return)
		core.core.event.keydown['escape'].bind(self.k_escape)
	
	def add_option(self, option):
		option.rect.move_ip(self.pos)
		option.rect.move_ip(0, 45*self.i)
		self.g.add(option)
		self.i+=1
		self.options.append(option)
		self.visible_options = self.options[self.minvisible:self.maxvisible]
		
	def update(self):
		self.g.draw(core.core.video.get_screen())

		
	def no_out(self):
		#actuacion en caso de que se salga del array
		if self.menu_en_bucle:
			self.position = self.position%len(self.options)
		else:
			if self.position < 0:
				self.position = 0
			elif self.position >= len(self.options):
				self.position = len(self.options)-1
		
		if self.position >= (self.maxvisible):
			self.minvisible = self.position-self.nvisibles+1
			self.maxvisible = self.position+1
			self.visible_options = self.options[self.minvisible:self.maxvisible]
			
		if self.position <= (self.minvisible):
			self.minvisible = self.position
			self.maxvisible = self.position+self.nvisibles
			self.visible_options = self.options[self.minvisible:self.maxvisible]
			
	def change_options(self,options):
		self.options = options
		self.position = 0
		self.minvisible = 0
		self.maxvisible = self.nvisibles
		self.visible_options = self.options[self.minvisible:self.maxvisible]
		
	def down(self):
		self.position += 1
		self.no_out()
		
	def up(self):
		self.position -= 1
		self.no_out()
		
	def obtain_position(self):
		return self.position
		
	def k_escape(self, event, data):
		self.activate = not self.activate
		return True
	
	def k_return(self, event, data):
		if self.activate or self.persistant:
			self.options[self.position].select()
	
	def k_space(self, event, data):
		if self.activate or self.persistant:
			self.options[self.position].select()
					
	
	def k_up(self, event, data):
		if self.activate or self.persistant:
			self.options[self.position].hover_off()
			self.up()
			self.options[self.position].hover_on()
			
		
	def k_down(self, event, data):
		if self.activate or self.persistant:
			self.options[self.position].hover_off()
			self.down()
			self.options[self.position].hover_on()
		

	def seleccionar(self,n):
		pass