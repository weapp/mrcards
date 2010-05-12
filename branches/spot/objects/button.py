from library.stdmodules import module
from library import core
import pygame
from library import event
import pressable
import div

t=0
def i():
	global t
	while 1:
		t+=1
		yield t
i = i()


class button(div.div, pressable.Pressable):
	def __init__(self, parent, func, **kws):
		div.div.__init__(self, parent, **kws)
		pressable.Pressable.__init__(self)
		self.func = func
		self.press.bind(self.__onpress, self.__unpress)
		self.mousebuttonup.bind(self.__click)
		self.i = i.next()
		
	def __onpress(self, event, data):
		self.text_offset_y += 2
		self.update_surface()
		print "x"
		import ctypes
		import win32con
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_LBUTTONUP, 0, 0);
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_NCLBUTTONDOWN, win32con.HTCAPTION, 0)
	
	def __click(self, event, data):
		#print "%s: click!" % self.i
		#core.core.get_app()['SceneManager'].change_scene(self.func)
		exec(self.func)
		
	def __unpress(self, event, data):
		self.text_offset_y -= 2
		self.update_surface()
