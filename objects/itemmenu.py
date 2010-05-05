import pygame
from library.stdmodules import module
import pressable
from library import core

class itemmenu(pygame.sprite.Sprite, module.Module, pressable.Pressable):
	def __init__(self, parent, name, func):
		module.Module.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		pressable.Pressable.__init__(self)
		self.name = name
		self.parent = parent
		f = pygame.font.Font("font.ttf", 40)
		self.imageon = f.render(name, True, (255, 200, 125))
		self.image = self.imageoff = f.render(name, True, (255, 125, 0))
		self.rect = self.image.get_rect()
		self.func = func
		
		
		self.hover.bind(self.onhover_handler, self.offhover_handler)
		self.click.bind(self.onclick, None)
		
		self.ishovered = False
		
		parent.add_option(self)
	
	def hover_on(self):
		self.image = self.imageon
		
	def hover_off(self):
		self.image = self.imageoff
	
	def onhover_handler(self, *args):
		self.hover_on()
		
	def offhover_handler(self, *args):
		self.hover_off()
		
	def change(self, *args):
		self.image, self.image2 = self.image2, self.image
	
	def onclick(self, *args):
		self.select()
		
	def select(self):
		core.core.get_app()['SceneManager'].change_scene(self.func)
		
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