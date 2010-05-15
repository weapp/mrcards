import button
import div
from library import core
import os

class song(button.button):
	def __init__(self, parent, file, i):
		button.button.__init__(self, parent, 'core.core.get_app().find("#reproductor").select("'+file+'",'+str(i)+')')
		self.title = div.div(self, content=file[:-4], kind="title")
		self.info = div.div(self, content="%0.2fMB" % (os.path.getsize("music/" + file)/1024.0/1024.0), kind="info" )
		
	def _button__click(self, event, data):
		if 'selected' in self.p.actual:
			core.core.get_app().find("#reproductor").play()
		else:
			for box in self.parent.parent.box:
				for child in box.get_childs():
					if 'selected' in child.p.actual:
						child.p.actual.remove('selected')
						child.update_position()
						child.title.p.actual.remove('selected')
						child.title.update_position()
			self.p.actual.append('selected')
			self.update_position()
			self.title.p.actual.append('selected')
			self.title.update_position()
			button.button._button__click(self, event, data)