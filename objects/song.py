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
			for child in self.parent.get_childs():
					child.p.pop('selected')
					child.title.p.pop('selected')
			self.p.push('selected')
			self.title.p.push('selected')
			button.button._button__click(self, event, data)