import div
import pressable
import ctypes
import win32con
import pygame


class move(div.div, pressable.Pressable):
	def __init__(self, parent, **kws):
		div.div.__init__(self, parent, **kws)
		pressable.Pressable.__init__(self)
		self.mousebuttondown.bind(self.__onpress)
		
	def __onpress(self, event, data):
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_LBUTTONUP, 0, 0);
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_NCLBUTTONDOWN, win32con.HTCAPTION, 0)