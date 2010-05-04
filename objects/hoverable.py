from library import core
from library.stdmodules.controller import event

class Hoverable:
	def __init__(self):
		self.onhover = event.Event("onhover")
		self.offhover = event.Event("offhover")
		self.hover = event.EventPack(self.onhover, self.offhover)
		core.core.get_app().search("#BindingManager")[0].mousemotion.bind(self.__mousemotion)
		self.__prev_pos = (-1,-1)
		
	def __mousemotion(self, event, data):
		if hasattr(self,'rect') and self.rect.collidepoint(data['pos']) and not self.rect.collidepoint(self.__prev_pos):
			self.onhover(**data)
		if hasattr(self,'rect') and not self.rect.collidepoint(data['pos']) and self.rect.collidepoint(self.__prev_pos):
			self.offhover(**data)
		self.__prev_pos = data['pos']