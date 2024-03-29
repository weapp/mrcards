from library.stdmodules import module
from library import core
import pygame
import re
from library.resources.images import getImage
from library.resources.font import getFont
import properties

		
import random
j = lambda : [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 10]


class div(pygame.sprite.Sprite, module.Module):
	def __init__(self, parent=None, id=None, kind=None, content="", **kws):
		self.dirty = False
		if not kind is None:
			kind = kind.split(" ")
		module.Module.__init__(self, id, kind)
		pygame.sprite.Sprite.__init__(self)
		self.p = properties.properties(self)
		for attr, value in kws.iteritems():
			self.p.set(attr, value)
		self.content = content
		self.set_parent(parent)
		for style in core.core.get_app().search("style"):
			style.apply_to_elem(self)
		self.update_position()
			
	def set_dirty(self, value):
		self.__dirty = value
		if value and hasattr(self, 'rect'):
			t = self.calculate_rect()
			t = self.rect.move(t.x, t.y)
			self.add_dirty_rect(t)
			
	def get_dirty(self):
		return self.__dirty
	
	dirty = property(get_dirty, set_dirty)
	
	def add_dirty_rect(self, rect):
		#self.parent.add_dirty_rect(self.rect.union(rect))
		self.parent.add_dirty_rect(rect)
	
	def update_self_position(self,*args):
		self.container = self.rect = pygame.Rect(0, 0, self.p.get('width') , self.p.get('height'))
		
		if self.p.get('vertical_alignment') == "bottom":
			top = self.parent.get_container(self).h - (self.rect.h + self.p.get('margin')[3])
			height = self.p.get('height')
		elif self.p.get('vertical_alignment') == "top":
			top = self.p.get('margin')[1]
			height = self.p.get('height')
		else:
			top = self.p.get('margin')[1]
			height = self.parent.get_container(self).h - (self.p.get('margin')[1] + self.p.get('margin')[3])
				
		if self.p.get('horizontal_alignment') == "right":
			left = self.parent.get_container(self).w - (self.rect.w + self.p.get('margin')[2])
			width = self.p.get('width')
		elif self.p.get('horizontal_alignment') == "left":
			left = self.p.get('margin')[0]
			width = self.p.get('width')
		else:
			left = self.p.get('margin')[0]
			width = self.parent.get_container(self).w - (self.p.get('margin')[0] + self.p.get('margin')[2])
			
		height = max(0, height)
		width = max(0, width)
		
		self.rect = pygame.Rect(left, top, width, height)
		self.container = self.rect.move(self.parent.get_container(self).x, self.parent.get_container(self).y)
		bw = self.p.get('border_width')
		self.container = self.container.inflate(-bw[0] -bw[2], -bw[1] -bw[3])
		self.update_surface()
	
	def update_position(self,*args):
		self.update_self_position(self,*args)
		for child in self.get_childs():
			child.update_position()
	
	def update_surface(self):
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA | pygame.HWSURFACE)
		#self.image.fill(self.p.background_color)
		bgcolor = self.p.get('background_color')
		image = self.p.get('background_image')
		
		if image or self.content:
			center = list(self.image.get_rect().center)
		
		if bgcolor[3] != 0:
			self.image.fill(bgcolor)
			
		
		if image:
			image = getImage(image)
			imgrect0 = image.get_rect(center=center).copy()
			self.image.blit(image, imgrect0)
			
			if self.p.get('repeat_x'):
				imgrect1 = image.get_rect(center=center).copy()
				imgrect2 = image.get_rect(center=center).copy()
				imgrect1.move_ip(-imgrect1.w, 0)
				imgrect2.move_ip(imgrect1.w, 0)
				while self.rect.x < imgrect1.x + imgrect1.w:
					self.image.blit(image, imgrect1)
					imgrect1.move_ip(-imgrect1.w, 0)
				
				while self.rect.w > imgrect2.x:
					self.image.blit(image, imgrect2)
					imgrect2.move_ip(imgrect2.w, 0)
					
			if self.p.get('repeat_y'):
				imgrect1 = image.get_rect(center=center).copy()
				imgrect2 = image.get_rect(center=center).copy()
				imgrect1.move_ip(0, -imgrect1.w)
				imgrect2.move_ip(0, imgrect1.w)
				while self.rect.y < imgrect1.y + imgrect1.h:
					self.image.blit(image, imgrect1)
					imgrect1.move_ip(0, -imgrect1.h)
				
				while self.rect.h > imgrect2.y:
					self.image.blit(image, imgrect2)
					imgrect2.move_ip(0, imgrect2.h)
		
		bw = self.p.get('border_width')
		if bw:
			
			#pygame.draw.rect(self.image, self.p.get('border_color'), self.image.get_rect().inflate(-1*self.p.get('border_width'), -1*self.p.get('border_width')), self.p.get('border_width'))
			self.image.fill(self.p.get('border_color'), pygame.Rect(0, 0, bw[0], self.rect.h))    #left
			self.image.fill(self.p.get('border_color'), pygame.Rect(0, 0, self.rect.w, bw[1])) #top
			self.image.fill(self.p.get('border_color'), pygame.Rect(self.rect.w - bw[2], 0, bw[2], self.rect.h))
			self.image.fill(self.p.get('border_color'), pygame.Rect(0, self.rect.h - bw[3], self.rect.w, bw[3]))
		
		if self.content != "":
			self.f = getFont(self.p.get('font'), self.p.get('font_size'))
			self.f.set_bold(self.p.get('bold'))
			self.f.set_underline(self.p.get('underline'))
			self.f.set_italic(self.p.get('italic'))
			#self.p.text_offset_x, self.p.text_offset_y = 0, 0
			self.surface_content = self.f.render(self.content, True, self.p.get('color_content'))
			if self.p.get('text_align') == "left":
				center[0] = self.surface_content.get_rect().center[0]
			elif self.p.get('text_align') == "righr":
				center[0] = self.rect.w - self.surface_content.get_rect().center[0]
				
			if self.p.get('text_align') == "top":
				center[1] = self.surface_content.get_rect().center[1]
			elif self.p.get('text_align') == "bottom":
				center[1] = self.rect.h - self.surface_content.get_rect().center[1]
				
			center = center[0] + self.p.get('text_offset_x'), center[1] + self.p.get('text_offset_y')
			self.image.blit(self.surface_content, self.surface_content.get_rect(center=center))
		
				
	def move(self, rel):
		self.rect.move_ip(rel)
		self.container.move_ip(rel)
	
	def calculate_rect(self):
		video = core.core.video.get_screen()
		rect = self.parent.get_container(self).clip(video.get_rect())
		if rect.w == 0: rect = pygame.Rect(0,0,0,0)
		return rect
	
	def update(self, update_rect):
		video = core.core.video.get_screen()
		rect = self.calculate_rect() #parent
		intersection_rect = self.rect.move(rect.x, rect.y).clip(update_rect)
		subimage_rect = intersection_rect.move(-self.rect.x-rect.x, -self.rect.y-rect.y).clip(self.image.get_rect())
		if intersection_rect.w:
			video.blit(self.image.subsurface(subimage_rect), intersection_rect)
			
			for child in self.get_childs():
				child.update(update_rect)
		
		self.dirty = False
	def get_container(self, child):
		return self.container
		
	def get_clip_container(self, child):
		return self.get_container(child)
		
		