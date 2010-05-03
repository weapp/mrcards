class Event:
	def __init__(self, type=None):
		self.type = type
		self.binds = []

	def __call__(self, **data):
		for func in filter(None, self.binds):
			func(self, data)

	def bind(self, funccion):
		self.binds.append(funccion)

class EventDic:
	def __init__(self, type=None):
		self.type = type
		self.binds = {}
	def __getitem__(self,key):
		return self.binds.setdefault(key, Event(type))
		
class EventPack(Event):
	def __init__(self, ev1, ev2):
		self.type = "pack"
		self.ev1 = ev1
		self.ev2 = ev2
	
	def __call__(self, **data):
		self.ev1(**data)
		self.ev2(**data)
		
	def bind(self, fun1, fun2):
		self.ev1.bind(fun1)
		self.ev2.bind(fun2)
		
class EventPackDic:
	def __init__(self, ev1, ev2):
		self.type = "pack"
		self.binds = {}
		self.ev1 = ev1
		self.ev2 = ev2
	def __getitem__(self,key):
		return self.binds.setdefault(key, EventPack(self.ev1[key], self.ev2[key]))
		
def bind(event, *args, **kws):
	event.bind(*args, **kws)

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
