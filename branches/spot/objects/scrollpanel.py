import div
import button

class scrollpanel(div.div):
		
	def __init__(self, *args, **kws):
		div.div. __init__(self, *args, **kws)
		self.main = div.div(self, id="image")
		button1 = button.button(self, func="", vertical_alignment="bottom", height="20", background_color="#8888")
		button2 = button.button(self, func="", vertical_alignment="top", height="20", background_color="#8888")
		button1.hover.bind(self.up, self.stop)
		button2.hover.bind(self.down, self.stop)
		self.direction = 0
		self.add_child = self.append_child
		
	def up(self, event, data):
		self.direction = 1
		
	def down(self, event, data):
		self.direction = -1
		
	def stop(self, event, data):
		self.direction = 0
	
	def append_child(self, child):
		div.div.add_child(self,child)
		self.main = child
		
	def update(self):
		div.div.update(self)
		self.main.p.margin[1] += 5 * self.direction
		self.main.p.margin[3] -= 5 * self.direction
		self.main.p.border_width=1
		
		self.update_position()