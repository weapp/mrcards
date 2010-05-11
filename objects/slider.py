from library.stdmodules import module
from library import core
import pygame
from library import event
import dragable
import div


class slider(div.div, dragable.dragable):
	def __init__(self, parent, direction="horizontal", **kws):
		div.div.__init__(self, parent, **kws)
		dragable.dragable.__init__(self)
		
				
	def move(self, rel):
		rel = list(rel)
		rel[1] = 0
		div.div.move(self, rel)
		if self.rect.x < 0:
			self.container.move_ip((-self.rect.x, 0))
			self.rect.move_ip((-self.rect.x, 0))
		elif self.rect.x + self.rect.w > self.parent.container.w:
			
			#self.rect.x = self.rect.x - self.rect.x + self.parent.container.w - self.rect.w
			self.container.move_ip( ( -self.rect.x + self.parent.container.w - self.rect.w, 0))
			self.rect.move_ip( ( -self.rect.x + self.parent.container.w - self.rect.w, 0))
			
			#nuevo_x = antiguo_x + desplazamiento
			
			#self.container.move_ip((self.rect.x-self.parent.container.w, 0))
			#self.rect.move_ip((self.rect.x-self.parent.container.w, 0))
			
			#self.container.move_ip((self.rect.w, 0))
			#self.rect.move_ip((self.rect.w, 0))