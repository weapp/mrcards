from library import core
from library.stdmodules.controller import event

class Clickable:
	def __init__(self):
		self.mousebuttondown = event.Event("mousebuttondown")
		self.mousebuttonup = event.Event("mousebuttonup")
		self.click = event.EventPack(self.mousebuttondown, self.mousebuttonup)
		core.core.get_app().search("#BindingManager")[0].mousebuttondown.bind(self.__mousebuttondown)
		core.core.get_app().search("#BindingManager")[0].mousebuttonup.bind(self.__mousebuttonup)
		
	def __mousebuttondown(self, event, data):
		if hasattr(self,'rect') and self.rect.collidepoint(data['pos']):
			self.mousebuttondown(**data)
		
	def __mousebuttonup(self, event, data):
		if hasattr(self,'rect') and self.rect.collidepoint(data['pos']):
			self.mousebuttonup(**data)