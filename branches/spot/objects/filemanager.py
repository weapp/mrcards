from library import event
import os
import div
import vbox
import button

class directoryentry(button.button):
	def __init__(self, parent, func, *args, **kws):
		button.button.__init__(self, parent, func, *args, **kws)

class filemanager(div.div):
	def __init__(self, parent):
		div.div.__init__(self, parent)
		self.dirs = []
		self.files = []
		self.items = vbox.vbox(self)
		
		self.directory = "c:\\"
		
	def set_directory(self, directory):
		print directory
		self.__directory = directory
		self.actualize_items()
		
	def get_directory(self):
		return self.__directory
		
	directory = property(get_directory, set_directory)
	
	def actualize_items(self, *args, **kws):
	
		print self.directory, repr(self.directory)
		path, self.dirs, self.files = os.walk(self.directory).next()
		
		self.items.clear()
		for dir in self.dirs:
			directoryentry(self.items, "self.parent.parent.parent.set_directory(%s)" % repr(self.directory + dir), content=dir)
		for files in self.files:
			div.div(self.items, content=files)