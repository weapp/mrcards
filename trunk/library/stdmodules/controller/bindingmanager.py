from library.stdmodules import module
import pygame

class BindingManager(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.bind = {}
		self.bind['KeyDown']={}
		self.bind['KeyUp']={}
		self.id = "bindings"
		
	def new_event(self, event):
		t = pygame.event.event_name(event.type)
		if hasattr(event, 'key'):
			k = pygame.key.name(event.key)
		else:
			k = None
	
		if k in self.bind.get(t, {}):
			self.bind[t][k]()
			
	def bind(self, elem, type, fun):
		pass

"""
FUNCIONES
bind
one (solo funciona una vez)
trigger (lanza el envento)
unbind

UI
toggle (click1, click2, ....)
hover (onhover, offhover)
hover (onhover)
click
#dblclick

TECLADO
keydown
#keypress
keyup

RATON
mousedown
mousemove
mouseout
mouseover
mouseup
"""