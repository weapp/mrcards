from library.stdmodules import module
from library import core
import pygame
from library.stdmodules.controller import event
import pressable

class button(pygame.sprite.Sprite, module.Module, pressable.Pressable):
	def __init__(self, name, func):
		module.Module.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		pressable.Pressable.__init__(self)
		
		f = pygame.font.Font("data/font.ttf", 12)
		
		self.image2 = f.render(name, True, (0, 0, 0))
		self.rect = self.image2.get_rect().move(100,30).inflate(12, 12)
		self.image = pygame.Surface((self.rect.w,self.rect.h))
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,6))
		
		self.func = func
		self.g = pygame.sprite.Group()
		self.g.add(self)
				
		self.press.bind(self.__onpress, self.__unpress)
		self.mousebuttonup.bind(self.__click)
			
	def update(self):
		self.g.draw(core.core.video.get_screen())
		
	def __onpress(self, event, data):
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,8))
	
	def __click(self, event, data):
		print "click!"
		
	def __unpress(self, event, data):
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,6))