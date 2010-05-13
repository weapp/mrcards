import button
import div
from library import core
import os

SELECTED = [150, 150, 255, 255]
NONSELECTED = [105,105,105,70]

class song(button.button):
	def __init__(self, parent, file, i):
		button.button.__init__(self, parent, 'core.core.get_app().find("#reproductor").select("'+file+'",'+str(i)+')', vertical_alignment="top", height="28", margin="[8,%s,8,0]" % (8+i*35), color_content="[200,200,200,255]", background="[105,105,105,70]" )
		
		self.add_child(div.div(self, content=file[:-4], color_content="[255,255,255,255]",text_align="left",margin="[5,5,5,5]"))
		
		self.add_child(div.div(self, content="%0.2fMB" % (os.path.getsize("music/" + file)/1024.0/1024.0), color_content="[255,255,255,100]", margin="[0,5,5,5]", horizontal_alignment="right", width="50", background="[70,130,90,255]", border_color="[70,130,90,255]", border_width="3" ))
		
	def _button__click(self, event, data):
		if self.background == SELECTED:
			core.core.get_app().find("#reproductor").play()
		else:
			for child in self.parent.get_childs():
				if child.background != NONSELECTED:
					child.background = NONSELECTED
					ch = child.get_childs()[0]
					ch.color_content = [255,255,255,255]
					ch.surface_content = ch.f.render(ch.content, True, ch.color_content)
					ch.update_surface()
					child.update_surface()
			self.background = SELECTED
			
			ch = self.get_childs()[0]
			ch.color_content = [0,0,0,255]
			ch.surface_content = ch.f.render(ch.content, True, ch.color_content)
			ch.update_surface()
			self.update_surface()
			button.button._button__click(self, event, data)