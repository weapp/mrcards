from library.stdmodules import module
from library import core
import pygame
from library.resources.images import getImage

class dragable(pygame.sprite.Sprite, module.Module):
	def __init__(self, filename):
		module.Module.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		self.image = getImage(filename)
		self.rect = self.image.get_rect()
		self.g = pygame.sprite.Group()
		self.g.add(self)
		
		self.bind( "click", self.clickdown, self.clickup )
		
		self.bind( "mousemotion", self.motion )
		
		self.rect.move_ip(300, 300)
		
		self.mousepos=(0,0)
		self.mousedown=0
		
	def update(self):
		self.g.draw(core.core.video.get_screen())
	
	def clickdown(self, *args):
		self.mousedown=1
		self.mousepos=args[0].pos
	
	def clickup(self, *args):
		self.mousedown=0
		
	def motion(self, *args):
		if self.mousedown:
			self.rect.move_ip(args[0].pos[0] - self.mousepos[0], args[0].pos[1] - self.mousepos[1])
			self.mousepos = args[0].pos
