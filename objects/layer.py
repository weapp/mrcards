from library.stdmodules.apps import basicapp
from library import core
import pygame

class layer(basicapp.BasicApp):
	def p(self):
		return core.core.video.get_screen()
	image = property(p)
	
	def __init__(self, parent=None):
		basicapp.BasicApp.__init__(self)
		self.rectangles = [self.image.get_rect()]
		self.container = self.rect = core.core.video.get_screen().get_rect()
		core.core.event.videoresize.bind(self.update_position)
		
	def update_position(self,event, data):
		core.core.video.set_size((data['w'],data['h']))
		self.container = self.rect = pygame.Rect(0, 0, data['w'], data['h'])
		self.add_dirty_rect(self.image.get_rect())
		for child in self.get_all_childs():
			child.update_position()
		
	def get_container(self, child):
		return self.container
		
	def get_clip_container(self, child):
		return self.container
	
	def add_dirty_rect(self, rect):
		self.rectangles.append(rect)
		
	def update(self):
		if self.rectangles:
			t = self.rectangles[0].unionall(self.rectangles)
			self.rectangles = []
			for child in self.get_childs():
				child.update(t)