from library import core
from library.stdmodules import module
import pygame
import song
import vbox
import os

class pygame_repr:
	def __init__(self):
		self.paused = True
		self.init_pos = 0
		self.act = 0
		#self.lenght = pygame.mixer.Sound(song).get_length()
		
	def __busy(self):
		return pygame.mixer.music.get_busy() and not self.paused
	busy = property(__busy)
	
	def get_pos(self):
		return self.init_pos + pygame.mixer.music.get_pos()

	def pause(self):
		self.paused = True
		self.act = self.get_pos()
		pygame.mixer.music.stop()
	
	def play(self, song, pos = 0):
		if not pos and self.paused:
			pos = self.act
		self.init_pos = pos
		self.paused = False
		pygame.mixer.music.load(song)
		pygame.mixer.music.play(0, pos/1000.0)
		
class reproductor(module.Module):
	def __init__(self, parent=None):
		module.Module.__init__(self)
		self.id = "reproductor"
		self.repr = pygame_repr()
		self.selected_song = None
		onload = core.core.get_app().find('&SceneManager').get_childs()[0].onload
		onload.bind(self.cargar)
		self.lenght = 1
		self.last_busy = False
		
	def update(self):
		play = core.core.get_app().find('#play')
		
		if self.repr.busy:
			self.update_slide()
		
		if self.repr.busy and not self.last_busy:
			play.p.set('background_image', "pause")
			self.lat_busy = True
		elif not self.repr.busy and self.last_busy:
			play.p.set('background_image', "play")
			self.lat_busy = False
			
		play.update_surface()
		
	def update_slide(self):
			slide = core.core.get_app().find('#slider')
			pos = self.repr.get_pos()
			total = slide.parent.get_container(slide).w - slide.rect.w
			slide.move((-total,0))
			#pos = total*pos/self.lenght
			slide.move((pos/100,0))
		
	def slidermove(self):
		self.repr.pause()
		slide = core.core.get_app().find('#slider')
		self.play(pos=slide.rect.x*100)
		
	
	def select(self, song, i):
		self.selected_song = song
		self.selected_isong = i
	
	def play_pause(self, song=None):
		if self.repr.busy:
			self.repr.pause()
		else:
			self.play(song)
	
	def play(self, song=None, pos=0):
		if song is None: song = self.selected_song
		if song is None: return	
		song = "music/" + song
		self.repr.play(song, pos)
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
		self.lista = core.core.get_app().find('#lista')
		self.recargar()
	
	def recargar(self, event=None, data=None):
		self.lista.clear()
		path, dir, files = os.walk('music').next()
		for i, file in enumerate(files):
			song.song(self.lista, file, i)