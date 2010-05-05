from library import core
from library import event
import clickable
import hoverable
import pygame

class Pressable(clickable.Clickable, hoverable.Hoverable):
	def __init__(self):
		clickable.Clickable.__init__(self)
		hoverable.Hoverable.__init__(self)
		self.onpress = event.Event("onpress")
		self.unpress = event.Event("unpress")
		self.press = event.EventPack(self.onpress, self.unpress)
		self.click.bind(self.onclick, self.upclick)
		self.hover.bind(self.__onhover, self.__offhover)
		
	def onclick(self, event, data):
		self.onpress(**data)
		
	def upclick(self, event, data):
		self.unpress(**data)
	
	def __offhover(self, event, data):
		self.unpress(**data)
	
	def __onhover(self, event, data):
		if pygame.mouse.get_pressed()[0]:
			self.onpress(**data)