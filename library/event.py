import pygame

class EventManager:
	def __init__(self):
		self.clear()
	
	def clear(self):
		self.quit = Event("quit")
		self.activeevent = Event("activeevent")
		self.keydown = Event("keydown", "keyname")
		self.keyup = Event("keyup", "keyname")
		self.keypress = EventPack(self.keydown, self.keyup)
		self.mousemotion = Event("mousemotion")
		self.mousebuttonup = Event("mousebuttonup", "button")
		self.mousebuttondown = Event("mousebuttondown", "button")
		self.videoresize = Event("videoresize")
		
	def get_all_bindings(self):
		return self.quit, self.activeevent, self.keydown, self.keyup, self.keypress, \
		self.mousemotion, self.mousebuttonup, self.mousebuttondown, self.videoresize
		
	def get_set_bindings(self, quit, activeevent, keydown, keyup, keypress, \
		mousemotion, mousebuttonup, mousebuttondown, videoresize):
		
		self.quit = quit
		self.activeevent = activeevent
		self.keydown = keydown
		self.keyup = keyup
		self.keypress = keypress
		self.mousemotion = mousemotion
		self.mousebuttonup = mousebuttonup
		self.mousebuttondown = mousebuttondown
		self.videoresize = videoresize
		
	def new_event(self, event):
		if   event.type == pygame.QUIT: self.quit()
		elif event.type == pygame.ACTIVEEVENT: self.activeevent(gain=event.gain, state=event.state)
		elif event.type == pygame.KEYDOWN: self.keydown(keyname=pygame.key.name(event.key), unicode=event.unicode, key=event.key, mod=event.mod)
		elif event.type == pygame.KEYUP: self.keyup(keyname=pygame.key.name(event.key), key=event.key, mod=event.mod)
		elif event.type == pygame.MOUSEMOTION: self.mousemotion(pos=event.pos, rel=event.rel, buttons=event.buttons)
		elif event.type == pygame.MOUSEBUTTONUP: self.mousebuttonup(pos=event.pos, button=event.button)
		elif event.type == pygame.MOUSEBUTTONDOWN: self.mousebuttondown(pos=event.pos, button=event.button)		
		elif event.type == pygame.JOYAXISMOTION:pass #TODO completar todos los eventos
		elif event.type == pygame.JOYBALLMOTION:pass
		elif event.type == pygame.JOYHATMOTION:pass
		elif event.type == pygame.JOYBUTTONUP:pass
		elif event.type == pygame.JOYBUTTONDOWN:pass
		elif event.type == pygame.VIDEORESIZE: self.videoresize(size=event.size, w=event.w, h=event.h)
		elif event.type == pygame.VIDEOEXPOSE:pass
		elif event.type == pygame.USEREVENT:pass
		

class Event:
	def __init__(self, type=None, key=None):
		self.type = type     #tipo del evento
		self.binds = []      #manejadores de eventos
		self.key = key       #clave para la condicion, para ecentos condicionados mediante claves
		self.subbinds = {}   #diccionario para eventos condicionados mediante claves
		
	def __call__(self, **data):
		#actualizamos la lista de manejadores, para eliminar las funciones no validas
		self.binds = filter(None, self.binds)
		#llamamos a las funciones manejadoras
		for func in self.binds:
			func(self, data)
		#recorremos la listas de eventos condicionados mediante claves
		for key, event in self.subbinds.iteritems():
			if key == data[self.key]:
				event(**data)

	trigger = __call__
	
	def bind(self, function):
		self.binds.append(function)
		
	def one(self, function):
		self.bind(One(function))
		
	def toggle(self, functions):
		self.bind(Toggle(functions))
		
	def unbind(self, func):
		self.binds.remove(func)
		
	def __getitem__(self,key):
		return self.subbinds.setdefault(key, Event(type))
		
class EventPack:
	def __init__(self, ev1, ev2):
		self.type = "pack"
		self.binds = {}
		self.ev1 = ev1
		self.ev2 = ev2
		
	def __call__(self, **data):
		self.ev1(**data)
		self.ev2(**data)
		
	trigger = __call__
	
	def bind(self, fun1, fun2):
		self.ev1.bind(fun1)
		self.ev2.bind(fun2)
		
	def one(self, fun1, fun2):
		self.bind(One(fun1), One(fun2))
		
	def toggle(self, funs1, funs2):
		self.bind(Toggle(funs1), Toggle(funs2))
		
	def unbind(self, fun1, fun2):
		self.ev1.unbind(fun1)
		self.ev2.unbind(fun2)

	def __getitem__(self, key):
		return self.binds.setdefault(key, EventPack(self.ev1[key], self.ev2[key]))


def bind(event, *args, **kws):
	event.bind(*args, **kws)

def unbind(event, *args, **kws):
	event.unbind(*args, **kws)

	
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
	
	
if __name__ == "__main__":
	class lanzador:
		def __init__(self):
			self.event = Event("fin de la impresion")
			self.p_event = EventPack(self.event, self.event)
			
		def imprimir(self):
			print "imprimiendo"
			import time
			time.sleep(1)
			self.event(state="ok")

			
	class capturador:
		def __init__(self):
			self.lanzador = lanzador()
			self.lanzador.p_event.bind(self.prin, None)
			
		def prin(self, event, data):
			if event.type == "fin de la impresion":
				if data['state'] == "ok":
					print "fin print"
				else:
					print "fallo en la impresion"

		def imprimir(self):
			self.lanzador.imprimir()

	capturador().imprimir()
	
	
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