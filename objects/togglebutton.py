import button

class togglebutton(button.button):
	def __init__(self,*args,**kws):
		button.button.__init__(self,*args,**kws)
		
	def _button__click(self, event, data):
		if 'selected' in self.p.actual:
			self.p.pop('selected')
		else:
			self.p.push('selected')
		button.button._button__click(self, event, data)