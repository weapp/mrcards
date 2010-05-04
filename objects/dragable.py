from library.stdmodules import module
from library import core
import pygame
from library.resources.images import getImage
from library.stdmodules.controller import event
import clickable

class dragable(pygame.sprite.Sprite, module.Module, clickable.Clickable):
	def __init__(self, filename):
		module.Module.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		clickable.Clickable.__init__(self)
		
		self.image = getImage(filename)
		self.rect = self.image.get_rect()
		self.g = pygame.sprite.Group()
		self.g.add(self)
		
		#self.bind( "click", self.clickdown, self.clickup )
		
		self.click.bind(self.clickdown, self.clickup)
		core.core.get_app().search("#BindingManager")[0].mousemotion.bind(self.motion )
		self.rect.move_ip(300, 300)
		
		self.mousedown=0
	
	def update(self):
		self.g.draw(core.core.video.get_screen())
	
	def clickdown(self, event, data):
		self.mousedown=1
	
	def clickup(self, event, data):
		self.mousedown=0
		
	def motion(self, event, data):
		if self.mousedown:
			self.rect.move_ip(data['rel'])