import sys
import threading

import pygame

from library import core
from library.stdmodules.apps import extendedapp
from library.stdmodules import module

class obj(module.Module):
	def __init__ (self, char="#"):
		module.Module.__init__(self)
		#print args, kws
		self.i=True
		self.char=char
		pass
		
		if self.char == "#":
			threading.Timer(4.0, self.inhabilitar)
	
	def inhabilitar():
		self.char="X"

	def __repr__(self):
		return "< %s >" % self.char
		
	def __str__(self):
		return "< %s >" % self.char
		
	def update(self):
		module.Module.update(self)
		sys.stdout.write('['+self.char*self.i+" "*(59-self.i)+']')
		sys.stdout.flush()
		sys.stdout.write('\r')
		self.i = (self.i + 1) % 60
		
		if self.char == "X":
			raise
		
class factory(object):
	def __init__(self):
		pass
		
	def obj(self,*args,**kws):
		return obj(*args,**kws)
	
c=core.Core()
app=extendedapp.ExtendedApp(factory())
app.get_childs('#SceneManager')[0].charge_and_change_scene('scena1', 'example2.xml')

def th():
	app.get_childs('#SceneManager')[0].charge_and_change_scene('scena1', 'example.xml')

threading.Timer(3.0, th).start()

"""
def th():
	print
	print "---"
	print "\n".join(map(repr,app.get_childs('*')))
	print "---"
	print

threading.Timer(4.1, th).start()
"""

core.FLAGS ^= pygame.RESIZABLE
c.set_size((150,150))
c.set_app(app)
c.start()