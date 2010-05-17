from library import core
from library.stdmodules import scenemanager
from library.stdmodules.apps import basicapp
from library.stdmodules.apps import extendedapp
import objects

import pygame

try:
	import sys
	if not "framed" in sys.argv:
		import ctypes, win32con
		core.core.video.flags |= pygame.NOFRAME
except:
	pass

core.core.video.set_size((800,600))

screen=core.core.video.get_screen()

class factory:
	def list(self,*arg): return arg
	def __getattr__(self, name):
		return getattr(getattr(objects, name), name)

factory = factory()

core.core.ticks = 40

app = extendedapp.ExtendedApp(factory)

sm = app.find('&SceneManager')

core.core.set_app(app)

sm.charge_and_change_scene("menu", "data/menu.xml")
sm.charge_and_change_scene("spot", "data/spot2.xml")

core.core.start()