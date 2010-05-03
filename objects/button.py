from library.stdmodules import module
from library import core
import pygame
from library.stdmodules.controller import event

class button(pygame.sprite.Sprite, module.Module):
	def __init__(self, name, func):
		module.Module.__init__(self)
		pygame.sprite.Sprite.__init__(self)
		f = pygame.font.Font("data/font.ttf", 12)
		
		self.image2 = f.render(name, True, (0, 0, 0))
		self.rect = self.image2.get_rect().move(100,30).inflate(12, 12)
		self.image = pygame.Surface((self.rect.w,self.rect.h))
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,6))
		
		self.func = func
		
		self.g = pygame.sprite.Group()
		self.g.add(self)
		
		self.mousebuttondown = event.Event("mousebuttondown")
		self.mousebuttonup = event.Event("mousebuttonup")
		self.click = event.EventPack(self.mousebuttondown, self.mousebuttonup)
		core.core.get_app().search("#BindingManager")[0].mousebuttondown.bind(self.__mousebuttondown)
		core.core.get_app().search("#BindingManager")[0].mousebuttonup.bind(self.__mousebuttonup)
		self.click.bind(self.onclick, self.upclick)
		#self.bind( "hover", self.onhover, self.offhover)
				
	def __mousebuttondown(self, event, data):
		if hasattr(self,'rect') and self.rect.collidepoint(data['pos']):
			self.mousebuttondown(**data)
		
	def __mousebuttonup(self, event, data):
		if hasattr(self,'rect') and self.rect.collidepoint(data['pos']):
			self.mousebuttonup(**data)
			
	def update(self):
		self.g.draw(core.core.video.get_screen())
		
	def onclick(self,*args):
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,8))
		
	def upclick(self,*args):
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,6))
		print "click!"
	
	def offhover(self, *args):
		self.image.fill((128,128,128))
		self.image.blit(self.image2, (6,6))
	
	def onhover(self, *args):
		if pygame.mouse.get_pressed()[0]:
			self.image.fill((128,128,128))
			self.image.blit(self.image2, (6,6))
		