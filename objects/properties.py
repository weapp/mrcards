import re

def dec(s):
	if len(s) == 8:
		return (int(s[0:2], 16),int(s[2:4], 16),int(s[4:6], 16), int(s[6:8], 16))
	elif len(s) == 4:
		return (int(s[0]*2, 16),int(s[1]*2, 16),int(s[2]*2, 16), int(s[3]*2, 16))
	elif len(s) == 3:
		return (int(s[0]*2, 16),int(s[1]*2, 16),int(s[2]*2, 16), 255)
	else:
		return (int(s[0:2], 16),int(s[2:4], 16),int(s[4:6], 16), 255)

class properties:
	def __init__(self, eventskey=[]):
		self.actual = ["default"]
		self.prop = {}
		self.sub = {}
		for key, event, event2 in eventskey:
			self.subscribe(key, event, event2)
		
	def subscribe(self, key, event, event2):
		self.sub.setdefault(key, properties())
		a1, a2 = self.action(key)
		event.bind(a1)
		event2.bind(a2)
	
	def action(self, key):
		def act(event, data):
			self.actual.append(key)
		def act2(event, data):
			if key in self.actual: self.actual.remove(key)
		return act, act2
		
	def __getattr__(self, attr):
		if self.sub.has_key(attr):		#pide una propiedad en un estado
			return self.sub[attr]		
		else:							#pide la prop actual
			r = None
			if self.actual[-1] != "default":								#no nos encontramos donde queremos la propiedad
				r = getattr(self.sub[self.actual[-1]], attr, None)					
			return r if not r is None else self.prop.get(attr, None)
		'''
		r = getattr(self.sub[self.actual[-1]],attr) if self.sub.has_key(self.actual[-1]) else self.prop.get(attr, None)
		if r is None:
			return self.sub[attr] if self.sub.has_key(attr) else self.prop.get(attr, None)
		else:
			return r
		'''

				
	def __setattr__(self, attr, value):
		if attr in ("actual", "prop", "sub"):
			self.__dict__[attr] = value
		else:
			self.prop[attr] = self.parse(attr, value)

	def parse(self, attr, value):
		if isinstance(value, basestring):
			if "width" in attr or "height" in attr:
				value = int(value)
			elif attr == "margin":
				value = map(int, re.match("\[(\d+),\s?(\d+),\s?(\d+),\s?(\d+)\]", value).groups())
			elif "color" in attr:
				if value.startswith("#"):
					value =	dec(value[1:])
				else:
					t = re.match("\[(\d+),\s?(\d+),\s?(\d+),\s?(\d+)\]", value)
					if t:
						value =  map(int, t.groups())
					else:
						value = map(int, re.match("\[(\d+),\s?(\d+),\s?(\d+)\]", value).groups()).append(255)
			elif attr in ("bold", "italic", "underline"):
				value = bool(value)
		return value
		
		
if __name__ == "__main__":
	from library import event
	e = event.Event()
	e2 = event.Event()
	p = properties( (("k", e, e2), ) )
	p.value1 = "default_value1"
	p.value2 = "default_value2"
	p.k.value2 = "k.value2"	
	assert p.actual[-1] == "default"
	assert p.value1 == "default_value1"
	assert p.value2 == "default_value2"
	e()
	assert p.actual[-1] == "k"
	assert p.value1 == "default_value1"
	assert p.value2 == "k.value2"
	e2()
	assert p.actual[-1] == "default"
	assert p.value1 == "default_value1"
	assert p.value2 == "default_value2"
	print "works!"