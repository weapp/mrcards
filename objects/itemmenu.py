import pygame
from library.stdmodules import module
import pressable
from library import core
import button

class itemmenu(button.button):
	def __init__(self, parent, name, func):
		button.button.__init__(self, parent, 'self.select()', content=name)
		self.sc = func
		self.name = name
		
		self.hover.bind(self.onhover_handler, self.offhover_handler)
		self.click.bind(self.onclick, None)
		
		self.ishovered = False
	
	def hover_on(self):
		self.p.push("hover")
		
		
	def hover_off(self):
		self.p.pop("hover")
	
	def onhover_handler(self, *args):
		self.hover_on()
		
	def offhover_handler(self, *args):
		self.hover_off()
		
	def change(self, *args):
		self.image, self.image2 = self.image2, self.image
	
	def onclick(self, *args):
		self.select()
		
	def select(self):
		core.core.get_app()['SceneManager'].change_scene(self.sc)
		
	def k_space(self, event, data):
		if self.activate or self.persistant:
			if self.editable:
				self.name += " "
			else:
				self.seleccionar(self.position)
					
	def k_backspace(self, event, data):
		if self.activate or self.persistant:
			if self.editable:
				self.name = self.name[:-1]
					
	def k_character(self, event, data):
		if self.activate or self.persistant:
			if self.editable:
				#if pygame.key.name(data['key']) in ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9","."):
				if pygame.key.name(data['key']) in "abcdefghijklmnopqrstuvwxyz0123456789.":
					keyname = pygame.key.name(data['key'])
					
					mod = pygame.key.get_mods()
												
					if mod in [pygame.KMOD_LSHIFT,pygame.KMOD_RSHIFT,pygame.KMOD_CAPS]:
						self.name += keyname.upper()
					else:
						self.name += keyname