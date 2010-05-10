from library import core
from library import event
import pygame

class Hoverable:
	def __init__(self):
		self.onhover = event.Event("onhover")
		self.offhover = event.Event("offhover")
		self.hover = event.EventPack(self.onhover, self.offhover)
		core.core.event.mousemotion.bind(self.__mousemotion)
		self.__prev_pos = (-1,-1)
		
	def __mousemotion(self, event, data):
		if hasattr(self,'parent') and hasattr(self.parent, 'container') and hasattr(self,'rect'):
			rect = self.container.clamp(self.parent.container).clip(self.parent.container)
			
			if rect.collidepoint(data['pos']) and not rect.collidepoint(self.__prev_pos):
				self.onhover(**data)
			if not rect.collidepoint(data['pos']) and rect.collidepoint(self.__prev_pos):
				self.offhover(**data)
			self.__prev_pos = data['pos']