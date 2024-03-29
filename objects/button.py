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
		self.p.subscribe('press', self.onpress, self.unpress)
		self.func = func
		self.press.bind(self.__onpress, self.__unpress)
		self.mousebuttonup.bind(self.__click)
		self.i = i.next()

	def __onpress(self, event, data):
		self.update_surface()
		
	def __unpress(self, event, data):
		self.update_surface()
	
	def __click(self, event, data):
		#print "%s: click!" % self.i
		#core.core.get_app()['SceneManager'].change_scene(self.func)
		exec(self.func)
		
