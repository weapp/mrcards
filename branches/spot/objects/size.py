import div
import clickable
import ctypes
import win32con
import pygame

# constants (copied from pyglet.window.win32.constants.py)
SW_HIDE = 0
SW_SHOWNORMAL = 1
SW_NORMAL = 1
SW_SHOWMINIMIZED = 2
SW_SHOWMAXIMIZED = 3
SW_MAXIMIZE = 3
SW_SHOWNOACTIVATE = 4
SW_SHOW = 5
SW_MINIMIZE = 6
SW_SHOWMINNOACTIVE = 7
SW_SHOWNA = 8
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_FORCEMINIMIZE = 11
SW_MAX = 11


class size(div.div, clickable.Clickable):
	def __init__(self, parent, **kws):
		div.div.__init__(self, parent, **kws)
		clickable.Clickable.__init__(self)
		self.mousebuttondown.bind(self.__onpress)
		
	def __onpress(self, event, data):
		#ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], SW_MINIMIZE);
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_LBUTTONUP, 0, 0);
		ctypes.windll.user32.SendMessageA(pygame.display.get_wm_info()['window'], win32con.WM_NCLBUTTONDOWN, win32con.HTGROWBOX, 0)