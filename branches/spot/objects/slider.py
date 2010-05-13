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
		
		self.__init_pos_mouse = (0,0)
		self.__init_pos_rect = self.rect.x, self.rect.y
		self.__init_pos_container = self.container.x, self.container.y
		
	def clickdown(self, event, data):
		dragable.dragable.clickdown(self,event,data)
		self.__init_pos_mouse = data['pos']
		self.__init_pos_rect = self.rect.x, self.rect.y
		self.__init_pos_container = self.container.x, self.container.y
	
	def clickup(self, event, data):
		dragable.dragable.clickup(self,event,data)
		
	def motion(self, event, data):
		if self.mousedown:
			self.restore()
			rel = data['pos'][0] - self.__init_pos_mouse[0], data['pos'][1] - self.__init_pos_mouse[1]
			self.move(rel)
	
	def restore(self):
		self.rect.x, self.rect.y = self.__init_pos_rect
		self.container.x, self.container.y = self.__init_pos_container
		
	def move(self, rel):
		rel = list(rel)
		rel[1] = 0
		div.div.move(self, rel)
		if self.rect.x < 0:
			self.container.move_ip((-self.rect.x, 0))
			self.rect.move_ip((-self.rect.x, 0))
		elif self.rect.x + self.rect.w > self.parent.container.w:
			self.container.move_ip( ( -self.rect.x + self.parent.container.w - self.rect.w, 0))
			self.rect.move_ip( ( -self.rect.x + self.parent.container.w - self.rect.w, 0))