import div

class vbox(div.div):
	def __init__(self, parent, *args, **kws):
		div.div.__init__(self, parent, *args, **kws)
		self.dirty = False
		self.containers = {}
		
	def get_container(self, child):
		if self.dirty:
			self.containers.clear()
		elif child in self.containers:
			return self.containers[child]

		div.div.update_self_position(self)
		childs = self.get_childs()
		container = self.container.copy()
		n = len(childs)
		if self.p.get('cell_height') is None:
			container.h = self.container.h/n
		else:
			container.h = self.p.get('cell_height')
			self.container.h = container.h * n
		if child in childs:
			container.move_ip(0, childs.index(child) * container.h)
		else:
			print "Acceso a hijo inesperado en vbox"
		self.containers[child] = container
		return container
		
	def add_child(self, child):
		self.dirty = True
		div.div.add_child(self, child)
		self.update_position()