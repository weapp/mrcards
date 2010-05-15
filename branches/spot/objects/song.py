import button
import div
from library import core
import os

class song(button.button):
	def __init__(self, parent, file, i):
		button.button.__init__(self, parent, 'core.core.get_app().find("#reproductor").select("'+file+'",'+str(i)+')', margin="[8,%s,8,0]" % (8+i*35))
		self.title = div.div(self, content=file[:-4], kind="title")
		self.info = div.div(self, content="%0.2fMB" % (os.path.getsize("music/" + file)/1024.0/1024.0), kind="info" )
		
	def _button__click(self, event, data):
		if "press" in self.p.actual:
			core.core.get_app().find("#reproductor").play()
		else:
			for child in self.parent.get_childs():
				if "press" in child.p.actual:
					child.p.actual.remove('press')
					child.update_position()
					child.title.p.actual.remove('press')
					child.title.update_position()
			self.p.actual.append('press')
			self.update_position()
			self.title.p.actual.append('press')
			self.title.update_position()
			button.button._button__click(self, event, data)