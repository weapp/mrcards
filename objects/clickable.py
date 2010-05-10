from library import core
from library import event

class Clickable:
	def __init__(self):
		self.mousebuttondown = event.Event("mousebuttondown")
		self.mousebuttonup = event.Event("mousebuttonup")
		self.click = event.EventPack(self.mousebuttondown, self.mousebuttonup)
		core.core.event.mousebuttondown[1].bind(self.__mousebuttondown)
		core.core.event.mousebuttonup[1].bind(self.__mousebuttonup)
		
	def __mousebuttondown(self, event, data):
		if hasattr(self,'parent') and hasattr(self.parent, 'container') and hasattr(self,'rect'):
			rect = self.container.clamp(self.parent.container).clip(self.parent.container)
			if rect.collidepoint(data['pos']):
				self.mousebuttondown(**data)
		
	def __mousebuttonup(self, event, data):
		if hasattr(self,'parent') and hasattr(self.parent, 'container') and hasattr(self,'rect'):
			rect = self.container.clamp(self.parent.container).clip(self.parent.container)
			if rect.collidepoint(data['pos']):
				self.mousebuttonup(**data)