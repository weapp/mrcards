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
		self.__press = 0
		
	def onclick(self, event, data):
		self.__press = 1
		self.onpress(**data)
		return True
		
	def __onhover(self, event, data):
		if pygame.mouse.get_pressed()[0]:
			self.__press = 1
			self.onpress(**data)
			
	def upclick(self, event, data):
		self.__press = 0
		self.unpress(**data)
	
	def __offhover(self, event, data):
		if self.__press == 1:
			self.unpress(**data)
		self.__press = 0
	