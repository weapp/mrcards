from library.stdmodules import module
from library import core
import pygame
from library import event
import clickable
import div
import ctypes, win32con

class sizer(div.div, clickable.Clickable):
	def __init__(self, parent, *args, **kws):
		div.div.__init__(self, parent, *args, **kws)
		clickable.Clickable.__init__(self)
		self.click.bind(self.clickdown, self.clickup)
		core.core.event.mousemotion.bind(self.motion)
		core.core.event.mousebuttonup[1].bind(self.clickup)
		self.mousedown=0
		self.size = [0,0]
		self.size[0] = self.t1 = core.core.video.get_screen().get_rect().w
		self.size[1] = self.t1 = core.core.video.get_screen().get_rect().h
		
	
	def clickdown(self, event, data):
		self.mousedown=1
	
	def clickup(self, event, data):
		self.mousedown=0
		core.core.video.set_size(self.size)
		core.core.event.videoresize(w=self.size[0],h=self.size[1])
		
	def motion(self, event, data):
		if self.mousedown:
			self.size[0] += data['rel'][0]
			self.size[1] += data['rel'][1]
			ctypes.windll.user32.MoveWindow(pygame.display.get_wm_info()['window'], 0, 0, self.size[0], self.size[1], 1)
			#SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_NCLBUTTONDOWN, win32con.HTCAPTION, 0)
			