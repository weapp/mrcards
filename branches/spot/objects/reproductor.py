from library import core
from library.stdmodules import module
import pygame
import button
import div
import os

class pygame_repr:
	def __init__(self):
		self.paused = True
		#self.lenght = pygame.mixer.Sound(song).get_length()
		
	def __busy(self):
		return pygame.mixer.music.get_busy() and not self.paused
	busy = property(__busy)
	
	def get_pos(self):
		return pygame.mixer.music.get_pos()

	def pause(self):
		self.paused = True
		pygame.mixer.music.pause()
	
	def play(self, song):
		self.paused = False
		pygame.mixer.music.load(song)
		pygame.mixer.music.play()
		
class reproductor(module.Module):
	def __init__(self):
		module.Module.__init__(self)
		self.id = "reproductor"
		self.repr = pygame_repr()
		self.selected_song = None
		onload = core.core.get_app().find('#SceneManager').get_childs()[0].onload
		onload.bind(self.cargar)
		self.lenght = 1
		
	def update(self):
		play = core.core.get_app().find('#play')
		if self.repr.busy:
			play.background_image = "pause"
			self.update_slide()
		else:
			play.background_image = "play"
		play.update_surface()
		
	def update_slide(self):
			slide = core.core.get_app().find('#slider')
			pos = self.repr.get_pos()
			total = slide.parent.container.w - slide.rect.w
			slide.move((-total,0))
			#pos = total*pos/self.lenght
			slide.move((pos/100,0))
		
	
	def select(self, song, i):
		self.selected_song = song
		self.selected_isong = i
	
	def play(self, song=None):
		if self.repr.busy:
			self.repr.pause()
		else:
			if song is None: song = self.selected_song
			if song is None: return
			song = "music/" + song
			self.repr.play(song)
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
		
	def cargar(self, event=None, data=None):
		#main = core.core.get_app().find('#SceneManager').get_childs()[0][1].get_childs()[0].get_childs()[2].get_childs()[1]
		main = core.core.get_app().find('#main')
		
		self.lista = div.div(main, margin = "[15,15,15,15]")		
		main.add_child(self.lista)
		self.recargar()
	
	def recargar(self, event=None, data=None):
		self.lista.clear()
		path, dir, files = os.walk('music').next()
		for i, file in enumerate(files):
			self.lista.add_child(button.button(self.lista, 'core.core.get_app().find("#reproductor").select("'+file+'",'+str(i)+')', content=file, vertical_alignment="top", height="20", margin="[5,%s,5,0]" % (5+i*25), color_content="[255,255,255,255]", background="[105,105,105,70]" ))