from library import core
import re
from library.stdmodules import module

class cmp:
	def __init__(self, elem):
		self.elem = elem
	def __call__(self, x):
		return x == self.elem
		
class style(module.Module):
	def __init__(self,parent, file):
		module.Module.__init__(self)
		self.scene = core.core.get_app().find('&SceneManager').get_childs()[0]
		self.scene.onload.bind(self.load)
		self.file = file
		self.load = False
		self.cached = False
		
	def load(self, event, data):
		self.load = True
		self.apply_to_elems()
	
	def apply_to_elem(self, elem):
		self.apply_to_elems(cmp(elem))
	
	def apply_to_elems(self, filter = None):
		if self.load:
			for selectors, properties in self.get_properties():
				for selector in selectors:
					if ":" in selector:
						selector, onevent = selector.split(":")
					else:
						onevent = None
					for item in self.scene.search(selector):
						if filter is None or filter(item):
							for prop in properties:
								prop = prop.split(":")
								item.p.get_sub(onevent).set(prop[0], prop[1])
							item.update_position()
	
	def get_propieties(self):
		if not self.cached:
			self.cache = list(get_propieties)
			self.cached = True
		return self.cache
			
	
	def get_properties(self):
		f = file("data/" + self.file + ".css").read()
		expr="([^{]*)({[^}]*})"
		
		end = 0
		while True:
			f = f[end:]
			r = re.search(expr, f)
			if r is None:
				return
			end = r.end()
			
			g = r.groups()
			selectors = [selector.strip() for selector in g[0].split(',')]
			yield selectors, list(self._parse_properties(g[1]))
			
	def _parse_properties(self, properties):
		expr="([^\n;]*);"
		end = 0
		while True:
			properties = properties[end:]
			r = re.search(expr, properties)
			if r is None:
				return
			end = r.end()
			yield  r.groups()[0].strip()
		
		
	
	def update(self):
		pass
	
	def draw(self):
		pass