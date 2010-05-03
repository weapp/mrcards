from library.stdmodules import module
import pygame
from event import Event, EventPack, EventDic, EventPackDic

class BindingManager(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.quit = Event("quit")
		self.activeevent = Event("activeevent")
		self.keydown = EventDic("keydown")
		self.keyup = EventDic("keyup")
		self.keypress = EventPackDic(self.keydown, self.keyup)
		self.mousemotion = Event("mousemotion")
		self.mousebuttonup = Event("mousebuttonup")
		self.mousebuttondown = Event("mousebuttondown")
		self.videoresize = Event("videoresize")
		
		
		
	def new_event(self, event):
		if event.type == pygame.QUIT: self.quit()
		elif event.type == pygame.ACTIVEEVENT: self.activeevent(gain=event.gain, state=event.state)
		elif event.type == pygame.KEYDOWN: self.keydown[pygame.key.name(event.key)](unicode=event.unicode, key=event.key, mod=event.mod)
		elif event.type == pygame.KEYUP: self.keyup[pygame.key.name(event.key)](key=event.key, mod=event.mod)
		elif event.type == pygame.MOUSEMOTION: self.mousemotion(pos=event.pos, rel=event.rel, buttons=event.buttons)
		elif event.type == pygame.MOUSEBUTTONUP: self.mousebuttonup(pos=event.pos, button=event.button)
		elif event.type == pygame.MOUSEBUTTONDOWN: self.mousebuttondown(pos=event.pos, button=event.button)		
		elif event.type == pygame.JOYAXISMOTION:pass
		elif event.type == pygame.JOYBALLMOTION:pass
		elif event.type == pygame.JOYHATMOTION:pass
		elif event.type == pygame.JOYBUTTONUP:pass
		elif event.type == pygame.JOYBUTTONDOWN:pass
		elif event.type == pygame.VIDEORESIZE: self.videoresize(size=event.size, w=event.w, h=event.h)
		elif event.type == pygame.VIDEOEXPOSE:pass
		elif event.type == pygame.USEREVENT:pass
		
	def trigger(self, obj, type_ , event=None):
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
			
	
	def __bind(self, obj, type_, func):
		obj._binds.setdefault(type_, []).append(func)
		
	def bind(self, obj, type_, func1, func2 = None):
		print "\nself:%s\nobj:%s\ntype:%s\nfunc:%s\n" % (self, obj, type_, func1)
		exit()
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