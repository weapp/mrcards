import sys
import os
import time

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
		
class Menu(module.Module):
	def __init__(self,opciones, *args, **kws):
		module.Module.__init__(self)
		self.opciones=opciones
		self.opciones[0].onHover()
		
	def draw(self):
		os.system('cls')
		print "\n".join(map(str,self.opciones))
		time.sleep(1)

class ControllerMenu(module.Module):
	def __init__(self, data, drawer):
		pass

class ItemMenu(module.Module):
	def __init__(self, name, option, *args, **kws):
		module.Module.__init__(self)
		self.name=name
		self.option=option
		self.hover=False
		
	def select(self):
		exec option
	
	def onHover(self):
		self.hover=True
		
	def outHover(self):
		self.hover=False

	def __str__(self):
		return " [%s] %s"%('x' if self.hover else " ",self.name)
		
class factory(object):
	def __init__(self):
		pass
	
	def list(self,*args):
		return args
		
	def obj(self,*args,**kws):
		return obj(*args,**kws)
	
	def ItemMenu(self,*args,**kws):
		return ItemMenu(*args,**kws)
		
	def Menu(self,*args,**kws):
		return Menu(*args,**kws)
	
c=core.Core()
app=extendedapp.ExtendedApp(factory())
app.get_childs('#SceneManager')[0].charge_and_change_scene('scena1', 'menu.xml')
core.FLAGS ^= pygame.RESIZABLE
c.set_size((150,150))
c.set_app(app)
c.start()