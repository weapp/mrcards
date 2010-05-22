from library.stdmodules import module
from library import core
import pygame
from library import event
import draggable
import div
from library.resources.images import getImage


class imagedraggable(div.div, draggable.draggable):
	def __init__(self, parent, onup="", **kws):
		div.div.__init__(self, parent, **kws)
		w, h = getImage(self.p.get('background_image')).get_rect().size
		self.p.set('vertical_alignment', "top")
		self.p.set('horizontal_alignment', "left")
		self.p.set('width', w)
		self.p.set('height', h)
		self.update_position()
		draggable.draggable.__init__(self)
		self.onup = onup
		self.__init_pos_mouse = (0,0)
		self.__init_pos_rect = self.rect.x, self.rect.y
		self.__init_pos_container = self.container.x, self.container.y
	

	def clickdown(self, event, data):
		draggable.draggable.clickdown(self,event,data)
		self.__init_pos_mouse = data['pos']
		self.__init_pos_rect = self.rect.x, self.rect.y
		self.__init_pos_container = self.container.x, self.container.y
	
	def clickup(self, event, data):
		if self.mousedown:
			exec(self.onup)
		draggable.draggable.clickup(self,event,data)
		
	def motion(self, event, data):
		if self.mousedown:
			self.restore()
			rel = data['pos'][0] - self.__init_pos_mouse[0], data['pos'][1] - self.__init_pos_mouse[1]
			self.move(rel)
	
	def restore(self):
		self.rect.x, self.rect.y = self.__init_pos_rect
		self.container.x, self.container.y = self.__init_pos_container
	
		self.update_surface()