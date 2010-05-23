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

def parse_margin(s):
	t = re.match("(\d+)[,\s]\s?(\d+)[,\s]\s?(\d+)[,\s]\s?(\d+)", s)
	if not t is None:
		t = map(int, t.groups())
		return t
	t = re.match("(\d+)[,\s]\s?(\d+)[,\s]\s?(\d+)", s)
	if not t is None:
		t = map(int, t.groups())
		t.append(t[1])
		return t
	t = re.match("(\d+)[,\s]\s?(\d+)", s)
	if not t is None:
		t = map(int, t.groups())
		t *= 2
		return t
	t = re.match("(\d+)", s)
	if not t is None:
		t = map(int, t.groups())
		t *= 4
		return t
	
class properties:
	def __init__(self, parent=None, eventskey=[]):
		self.parent=parent
		self.actual = []
		self.prop = {}
		self.sub = {}
		for key, event, event2 in eventskey:
			self.subscribe(key, event, event2)
		
	def subscribe(self, key, event, event2):
		self.sub.setdefault(key, properties(self.parent))
		a1, a2 = self.action(key)
		event.bind(a1)
		event2.bind(a2)
	
	def push(self, key):
		self.actual.append(key)
		if self.get_sub(key).prop:
			if not self.parent is None: self.parent.update_position()
		self.parent.dirty = True
		self.update_surface()
		
	def pop(self, key):
		if key in self.actual:
			self.actual.remove(key)
			if not self.parent is None: self.parent.update_position()
		self.parent.dirty = True
		self.update_surface()
	
	def get_sub(self, sub):
		if sub is None:
			return self
		else:
			return self.sub.setdefault(sub, properties(self.parent))
	
	def action(self, key):
		def act(event, data):
			self.push(key)
		def act2(event, data):
			self.pop(key)
		return act, act2
	
	def get(self, prop):
		r = None
		for elem in reversed(self.actual):
			r = self.get_sub(elem).get(prop)
			if not r is None: break
		return r if not r is None else self.prop.get(prop, None)
		
	def set(self, prop, value):
		prop = prop.replace("-","_")
		self.prop[prop] = self.parse(prop, value)
		self.update_surface()
		self.parent.dirty = True
	
	def update_surface(self):
		if self.parent:
			self.parent.dirty = True
			#self.parent.update_position()
	
	"""
	def __getattr__(self, attr):
		if self.sub.has_key(attr):		#pide una propiedad en un estado
			return self.sub[attr]		
		else:							#pide la prop actual
			r = None
			for elem in reversed(self.actual):
				r = getattr(self.get_sub(elem), attr, None)
				if not r is None: break
			return r if not r is None else self.prop.get(attr, None)
		'''
		r = getattr(self.sub[self.actual[-1]],attr) if self.sub.has_key(self.actual[-1]) else self.prop.get(attr, None)
		if r is None:
			return self.sub[attr] if self.sub.has_key(attr) else self.prop.get(attr, None)
		else:
			return r
		'''

	def __setattr__(self, attr, value):
		if attr in ("actual", "prop", "sub", "parent"):
			self.__dict__[attr] = value
		else:
			#self.prop[attr] = self.parse(attr, value)
			raise Exception()
	"""

	
	def parse(self, attr, value):
		if isinstance(value, basestring):
			if attr in ("margin", "border_width"):
				if value.startswith("["):
					value = parse_margin(value[1:-1])
				else:
					value = parse_margin(value)
			elif "width" in attr or "height" in attr or "offset" in attr or "size" in attr:
				value = int(value)
			elif "color" in attr:
				if value.startswith("#"):
					value =	dec(value[1:])
				else:
					t = re.match("\[(\d+),\s?(\d+),\s?(\d+),\s?(\d+)\]", value)
					if t:
						value =  map(int, t.groups())
					else:
						value = map(int, re.match("\[(\d+),\s?(\d+),\s?(\d+)\]", value).groups()).append(255)
			elif attr in ("bold", "italic", "underline", "repeat_x", "repeat_y"):
				value = not value in ("0", "False", "false", "")
			elif not attr in ("font", "background-image"): #los nombres de archivos no deben pasarse a minuscula
				value = value.lower()
		return value
		
		
if __name__ == "__main__":
	from library import event
	e = event.Event()
	e2 = event.Event()
	p = properties( eventskey=(("k", e, e2), ) )
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