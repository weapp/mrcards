from library.stdmodules import module
from library import core
import pygame
from library import event
import clickable

class draggable(clickable.Clickable):
	def __init__(self, *args, **kws):
		clickable.Clickable.__init__(self, *args, **kws)
		self.click.bind(self.clickdown, self.clickup)
		core.core.event.mousemotion.bind(self.motion )
		
		core.core.event.mousebuttonup[1].bind(self.clickup)
		
		self.mousedown=0
	
	def clickdown(self, event, data):
		self.mousedown=1
	
	def clickup(self, event, data):
		self.mousedown=0
		
	def motion(self, event, data):
		if self.mousedown:
			self.move(data['rel'])