from library import core
from library.stdmodules import module
import pygame
from button import button

class reproductor(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.id = "reproductor"
		
	def play(self, song):
		song = "music/"+song
		pygame.mixer.music.load(song)
		pygame.mixer.music.play()
		#pygame.mixer.music.queue(song)
		'''
		print dir(pygame.mixer.music)
		print pygame.mixer.music.get_busy()
		#print pygame.mixer.music.get_pos()
		#pygame.mixer.music.play(0, 10)
		#print pygame.mixer.music.get_pos()
		pygame.mixer.music.load(song)
		print pygame.mixer.music.get_busy()
		'''
		
	def cargar(self):
		t = core.core.get_app().find('#SceneManager').get_childs()[0][1].get_childs()[0].get_childs()[2].get_childs()[1]
		t.clear()
		import os
		path, dir, files = os.walk('music').next()
		for i, file in enumerate(files):
			t.add_child(button(t, 'core.core.get_app().find("#reproductor").play("'+file+'")', content=file, vertical_alignment="top", height="50", margin="[5,%s,5,0]" % (5+i*55), background="[255,255,255,120]" ))