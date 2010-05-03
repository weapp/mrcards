from library.stdmodules import module
import pygame

class BindingManager(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.__hover = set()
		self.hover = set()
		self.objects = set()
		self.binds = {}
		self.__pos = (0,0)
		
		'''
		self.keydown = {}
		self.keyup = {}
		self.onhover = {}
		self.offhover = {}
		self.mousedown = {}
		self.mouseup = {}
		'''
	
	def execute(self, funcs, event):
		funcs = [func for func in funcs if func]
		for func in funcs:
			func(event)
	
	def update_hover(self, pos):
		self.__pos = pos
		self.__hover = self.hover
		self.hover = set()
		for elem in self.get_hover_elems():
			self.hover.add(elem)
		
	def get_hover_elems(self):
		for elem in self.objects:
			if hasattr(elem,'rect') and elem.rect.collidepoint(self.__pos):
				yield elem
	
	def get_onhover_elems(self):
		for elem in self.hover.difference(self.__hover):
			yield elem
	
	def get_offhover_elems(self):
		for elem in self.__hover.difference(self.hover):
			yield elem
		
	def get_pos(self): return self.__pos
	
	hover_elems = property(get_hover_elems)
	onhover_elems = property(get_onhover_elems)
	offhover_elems = property(get_offhover_elems)
	pos = property(get_pos, update_hover)
	
	def trigger(self, obj, type_ , event=None):
		'''
		self.keydown = {}
		self.keyup = {}
		self.onhover = {}
		self.offhover = {}
		self.mousedown = {}
		self.mouseup = {}
		'''
		
		t = type_.split(".")
		if type_ == 'mousemotion':
			self.pos = event.pos

			for elem in self.objects:
				if elem._binds.has_key('mousemotion'):
					self.execute(elem._binds['mousemotion'], event)

			for elem in self.onhover_elems:
				self.trigger(elem, 'onhover', event)

			for elem in self.offhover_elems:
				self.trigger(elem, 'offhover', event)
				#self.execute(elem._binds['mousemotion'], event)
			
		elif type_ == 'videoresize':
			for elem in self.objects:
				if elem._binds.has_key('videoresize'):
					self.execute(elem._binds['videoresize'], event)
					print elem
					
		elif type_ == 'onhover':
			self.execute(obj._binds.get('onhover', []), event)
			
		elif type_ == 'offhover':
			self.execute(obj._binds.get('offhover', []), event)
			
			
		elif t[0] == 'keydown':
			self.execute(obj._binds.get('keydown', {}).get(t[1], []), event)
		elif t[0] == 'keyup':
			self.execute(obj._binds.get('keyup', {}).get(t[1], []), event)
			
		elif type_ == "mouseup":
			self.execute(obj._binds.get('mouseup', []), event)
		elif type_ == "mousedown":
			self.execute(obj._binds.get('mousedown', []), event)
			
			
	
	def new_event(self, event):
		if event.type == pygame.QUIT: pass
		elif event.type == pygame.ACTIVEEVENT: pass
		elif event.type == pygame.KEYDOWN:
			for elem in self.objects:
				self.trigger(elem, 'keydown.%s' % pygame.key.name(event.key), event)
		elif event.type == pygame.KEYUP:
			for elem in self.objects:
				self.trigger(elem, 'keyup.%s' % pygame.key.name(event.key), event)
		elif event.type == pygame.MOUSEMOTION:
			self.trigger(self, 'mousemotion', event)
		elif event.type == pygame.MOUSEBUTTONUP:
			for elem in self.objects:
				if hasattr(elem, 'rect') and elem.rect.collidepoint(event.pos):
					self.trigger(elem, 'mouseup', event)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			for elem in self.objects:
				if hasattr(elem, 'rect') and elem.rect.collidepoint(event.pos):
					self.trigger(elem, 'mousedown', event)
		
		elif event.type == pygame.JOYAXISMOTION:pass
		elif event.type == pygame.JOYBALLMOTION:pass
		elif event.type == pygame.JOYHATMOTION:pass
		elif event.type == pygame.JOYBUTTONUP:pass
		elif event.type == pygame.JOYBUTTONDOWN:pass
		elif event.type == pygame.VIDEORESIZE:
			self.trigger(self, 'videoresize', event)
		elif event.type == pygame.VIDEOEXPOSE:pass
		elif event.type == pygame.USEREVENT:pass
	
	def __bind(self, obj, type_, func):
		obj._binds.setdefault(type_, []).append(func)
		
	def bind(self, obj, type_, func1, func2 = None):
		self.objects.add(obj)
		t = type_.split(".")
		if t[0] == "keypress":
			obj._binds.setdefault('keydown', {}).setdefault(t[1], []).append(func1)
			obj._binds.setdefault('keyup', {}).setdefault(t[1], []).append(func2)
		elif t[0] == "keydown":
			obj._binds.setdefault('keydown', {}).setdefault(t[1], []).append(func1)		
		elif t[0] == "keyup":
			obj._binds.setdefault('keyup', {}).setdefault(t[1], []).append(func1)
			
		elif type_ == "hover":
			self.__bind(obj,'onhover',func1)
			self.__bind(obj,'offhover',func2)
		elif type_ == "onhover":
			self.__bind(obj,'onhover',func1)
		elif type_ == "offhover":
			self.__bind(obj,'offhover',func1)
		elif type_ == "click":
			self.__bind(obj,'mousedown',func1)
			self.__bind(obj,'mouseup',func2)
		elif type_ == "mousedown":
			self.__bind(obj,'mousedown',func1)
		elif type_ == "mouseup":
			self.__bind(obj,'mousedown',func1)
			
		elif type_ == "mousemotion":
			self.__bind(obj,'mousemotion',func1)
			
		elif type_ == "videoresize":
			self.__bind(obj,'videoresize',func1)
	
	def unbind(self, obj, type_=None, func1=None):
		if not type_ and not func1:
			obj._binds.clear()
			if obj in self.objects:
				self.objects.remove(obj)
		elif not func1:
			del obj._binds[type_]
			if not len(obj._binds):
				self.objects.remove(obj)
		else:
			obj._binds[type_].remove(func1)
			if not len(obj._binds[type_]):
				del obj._binds[type_]
			if not len(obj._binds):
				self.objects.remove(obj)
				
	def one(self, obj, type_, func1, func2 = None):
		if func1:
			func1 = One(func1)
		if func2:
			func2 = One(func2)
		self.bind(obj, type_, func1, func2)
			
	def toggle(self, obj, type_, func1, func2 = None):
		if func1:
			func1 = Toggle(func1)
		if func2:
			func2 = Toggle(func2)
		self.bind(obj, type_, func1, func2)
			
				
	def link_key(self, key, name):
		down = pygame.event.Event(pygame.USEREVENT, {"link":True, "name":name, "key":key, "downup":"down"})
		up = pygame.event.Event(pygame.USEREVENT, {"link":True, "name":name, "key":key, "downup":"up"})
				
		self.bind(self, "%s.%s" % ("keydown",key), lambda: pygame.event.post(down))
		self.bind(self, "%s.%s" % ("keyup",key), lambda: pygame.event.post(up))
		
	def unlink_key(self, key, name):
		pass #buscar los que tengan key, name en keydown y keyup
		
class One:
	def __init__(self, func):
		self.active = True
		self.func = func
		
	def __call__(self, *args, **kws):
		self.active = False
		return self.func(*args, **kws)
		
	def __nonzero__(self):
		return self.active
		
class Toggle:
	def __init__(self, funcs):
		self.i = -1
		self.funcs = funcs
		
	def __call__(self, *args, **kws):
		self.i += 1
		if self.i == len(self.funcs): self.i=0
		return self.funcs[self.i](*args, **kws)
		
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