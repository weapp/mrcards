import div

class vbox(div.div):
	def __init__(self, parent, *args, **kws):
		div.div.__init__(self, parent, *args, **kws)
		self.box = []
		self.addchild = self.add_child
		self.add_child = self.append_child
		
	def append_child(self, child):
		if not self.box or child not in self.box[-1].get_childs():
			self.add_box().add_child(child)
			self.update_position()
	
	def add_box(self):
		self.add_child = self.addchild
		box = div.div(self)
		self.box.append(box)
		self.add_child = self.append_child
		return box
		
	def clear(self):
		div.div.clear(self)
		self.box = []
		
	def update_position(self, *args, **kws):
		div.div.update_self_position(self, *args, **kws)
		if hasattr(self, "box"):
			for i, box in enumerate(self.box):
				if self.p.cell_height is None:
					h = self.container.h/len(self.box)
				else:
					h = self.p.cell_height
					self.container.h = h*len(self.box)
				
				h = self.container.h/len(self.box)
				box.p.height = h
				box.p.vertical_alignment = "top"
				box.p.margin = "0,%s,0,0" % (i*h)
				
		for child in self.get_childs():
			child.update_position()