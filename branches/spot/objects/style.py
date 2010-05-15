from library import core
import re
from library.stdmodules import module

class style(module.Module):
	def __init__(self,parent, file):
		module.Module.__init__(self)
		self.scene = core.core.get_app().find('&SceneManager').get_childs()[0]
		self.scene.onload.bind(self.load)
		self.file = file
		
		
	def load(self, event, data):
		for selector, properties in self.get_properties():
			if ":" in selector:
				selector, onevent = selector.split(":")
			else:
				onevent = None
			for item in self.scene.search(selector):
				for prop in properties:
					prop = prop.split(":")
					setattr(item.p.get_sub(onevent), prop[0].replace("-","_"), prop[1])
				item.update_position()
	
	def apply_to_elem(self, elem):
		for selector, properties in self.get_properties():
			if ":" in selector:
				selector, onevent = selector.split(":")
			else:
				onevent = None
			for item in self.scene.search(selector):
				if elem == item:
					for prop in properties:
						prop = prop.split(":")
						setattr(item.p.get_sub(onevent), prop[0].replace("-","_"), prop[1])
					item.update_position()
	
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
			selector = g[0].strip()
			yield selector, list(self._parse_properties(g[1]))
			
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