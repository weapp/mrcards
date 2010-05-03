from library.stdmodules.apps import basicapp
from library import core
import pygame

class layer(basicapp.BasicApp):
	def __init__(self, *args):
		basicapp.BasicApp.__init__(self)
		self.rect = core.core.video.get_screen().get_rect()
		for elem in args:
			self.append(elem)
		
		self.bind("videoresize", self.update_position)
		
	def update_position(self,*args):
		if args:
			h = args[0].h
			w = args[0].w
			self.rect = pygame.Rect(0,0,w,h)		
		for child in self.get_all_childs():
			child.update_position()
			
