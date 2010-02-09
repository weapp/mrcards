from library.stdmodules import module
import pygame

class BindingManager(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.keydown = {}
		self.keyup = {}
		self.id = "bindings"
		self.hover = set()
		self.onhover = {}
		self.offhover = {}
		self.mousedown = {}
		self.mouseup = {}
		
	def new_event(self, event):
		#t = pygame.event.event_name(event.type)

		if event.type == pygame.QUIT:
			pass
		elif event.type == pygame.ACTIVEEVENT:
			pass
			
		elif event.type == pygame.KEYDOWN:
			func = self.keydown.get(pygame.key.name(event.key), None)
			if not func is None:
				func()
				
		elif event.type == pygame.KEYUP:
			func = self.keyup.get(pygame.key.name(event.key), None)
			if not func is None:
				func()
				
		elif event.type == pygame.MOUSEMOTION:
			self.__hover = self.hover
			self.hover = set()
			for elem in set(self.onhover.keys()).union(self.offhover.keys()):
				if elem.rect.collidepoint(event.pos):
					self.hover.add(elem)
			for elem in self.hover.difference(self.__hover):
				if elem in self.onhover:
					self.onhover[elem]()
			for elem in self.__hover.difference(self.hover):
				if elem in self.offhover:
					self.offhover[elem]()
					
		elif event.type == pygame.MOUSEBUTTONUP:
			for elem in set(self.mouseup.keys()):
				if elem.rect.collidepoint(event.pos):
					self.mouseup[elem]()
					
		elif event.type == pygame.MOUSEBUTTONDOWN:
			for elem in set(self.mousedown.keys()):
				if elem.rect.collidepoint(event.pos):
					self.mousedown[elem]()
		
		elif event.type == pygame.JOYAXISMOTION:
			pass
		elif event.type == pygame.JOYBALLMOTION:
			pass
		elif event.type == pygame.JOYHATMOTION:
			pass
		elif event.type == pygame.JOYBUTTONUP:
			pass
		elif event.type == pygame.JOYBUTTONDOWN:
			pass
		elif event.type == pygame.VIDEORESIZE:
			pass
		elif event.type == pygame.VIDEOEXPOSE:
			pass
		elif event.type == pygame.USEREVENT:
			pass
			
	
	def bind(self, obj, type_, func1, func2 = None):
		t = type_.split(".")
		if t[0] == "keypress":
			self.keydown[t[1]] = func1
			if not func2 is None:
				self.keyup[t[1]] = func2
		elif t[0] == "keydown":
			self.keydown[t[1]] = func1		
		elif t[0] == "keyup":
			self.keyup[t[1]] = func1
		
		elif type_ == "hover":
			self.onhover[obj] = func1
			if not func2 is None:
				self.offhover[obj] = func2
		elif type_ == "onhover":
			self.onhover[obj] = func1
		elif type_ == "offhover":
			self.offhover[obj] = func1
			
		elif type_ == "click":
			self.mousedown[obj] = func1
			if not func2 is None:
				self.mouseup[obj] = func2
		elif type_ == "mouse":
			self.mousedown[obj] = func1
			if not func2 is None:
				self.mouseup[obj] = func2
				
	def link_key(self, key, name):
		down = pygame.event.Event(pygame.USEREVENT, {"link":True, "name":name, "key":key, "downup":"down"})
		up = pygame.event.Event(pygame.USEREVENT, {"link":True, "name":name, "key":key, "downup":"up"})
				
		self.bind(self, "%s.%s" % ("keydown",key), lambda: pygame.event.post(down))
		self.bind(self, "%s.%s" % ("keyup",key), lambda: pygame.event.post(up))
		
	def unlink_key(self, key, name):
		pass #buscar los que tengan key, name en keydown y keyup
		
"""
FUNCIONES
bind
one (solo funciona una vez)
trigger (lanza el envento)
unbind

UI
toggle (click1, click2, ....)
#dblclick

TEECLADO
key (sin concretar la letra)

RATON
mousemove
mouseout
mouseover
"""