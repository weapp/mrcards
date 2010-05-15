import button

class togglebutton(button.button):
	def __init__(self,*args,**kws):
		button.button.__init__(self,*args,**kws)
		self.i=0
		
	def _button__click(self, event, data):
		self.i += 1
		if self.i == 2: self.i=0
		if self.i:
			self.p.actual.append('press')
		else:
			self.p.actual.remove('press')
		self.update_surface()
		button.button._button__click(self, event, data)
		