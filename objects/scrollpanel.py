import div
import button

class scrollpanel(div.div):
		
	def __init__(self, *args, **kws):
		div.div. __init__(self, *args, **kws)
		self.i = 0
		self.direction = 0
		self.b = True
		self.button1 = button.button(self, func="", vertical_alignment="bottom", height="20", background_color="#8888")
		self.button2 = button.button(self, func="", vertical_alignment="top", height="20", background_color="#8888")
		self.b = False
		self.main = div.div(self, id="image")
		self.button1.hover.bind(self.up, self.stop)
		self.button2.hover.bind(self.down, self.stop)
		#self.add_child = self.append_child
		
	def up(self, event, data):
		self.direction = 1
		
	def down(self, event, data):
		self.direction = -1
		
	def stop(self, event, data):
		self.direction = 0
	
	def append_child(self, child):
		div.div.add_child(self,child)
		self.main = child
		
	def get_container(self, child):
		if self.b or child == self.button1 or child ==self.button2:
			return self.container
		else:
			#child.p.margin[1] = self.i
			#child.p.margin[3] = -self.
			#return self.container
			return self.container.move(0, self.i)
		
		
	def get_clip_container(self, child):
		if self.b or child == self.button1 or child ==self.button2:
			return self.container
		else:
			#child.p.margin[1] = self.i
			#child.p.margin[3] = -self.
			#return self.container
			return self.container
	
	def update(self):
		div.div.update(self)
		self.i += self.direction
		#self.update_position()
		
	'''
	def update(self):
		div.div.update(self)
		self.main.p.margin[1] += 5 * self.direction
		self.main.p.margin[3] -= 5 * self.direction
		self.main.p.border_width=1
		
		self.update_position()
	'''