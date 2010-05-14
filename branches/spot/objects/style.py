from library import core

class style:
	def __init__(self, file):
		self.scene = core.core.get_app().find('&SceneManager').get_childs()[0]
		self.scene.onload.bind(self.load)
		self.file = file
		
		
	def load(self, event, data):
		pass
		
	def update(self):
		pass
	
	def draw(self):
		pass