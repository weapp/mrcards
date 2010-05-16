from library.stdmodules import module
from library import core
import pygame
import re
from library.resources.images import getImage
from library.resources.font import getFont
import properties

default = dict( color_content="[0,0,0,0]", width="0", height="0", vertical_alignment="", \
				horizontal_alignment="", margin="[0,0,0,0]", background_color="[80,80,80,0]", background_image=None, \
				border_color="[0,0,0,0]", border_width="0", overflow="hidden",\
				bold="", underline="", italic="", text_align="center", vertical_align="center", font="DroidSans", font_size=12 )

class div(pygame.sprite.Sprite, module.Module):
	
	def set_prop(self, attr, value):
		setattr(self.p, attr, value)
	
	def __init__(self, parent=None, id=None, kind=None, content="", **kws):
		if not kind is None:
			kind = kind.split(" ")
		module.Module.__init__(self, id, kind)
		pygame.sprite.Sprite.__init__(self)
		self.p = properties.properties(self)
		for attr, value in default.iteritems():
			self.set_prop(attr, value)
		for attr, value in kws.iteritems():
			self.set_prop(attr, value)
		self.content = content
		self.set_parent(parent)
		for style in core.core.get_app().search("style"):
			style.apply_to_elem(self)
		self.update_position()
		
	def update_self_position(self,*args):
		self.container = self.rect = pygame.Rect(0, 0, self.p.width , self.p.height)
		self.f = getFont(self.p.font, self.p.font_size)
		self.f.set_bold(self.p.bold)
		self.f.set_underline(self.p.underline)
		self.f.set_italic(self.p.italic)
		self.p.text_offset_x, self.p.text_offset_y = 0, 0
		
		if self.p.vertical_alignment.lower() == "bottom":
			top = self.parent.container.h - (self.rect.h + self.p.margin[3])
			height = self.p.height
		elif self.p.vertical_alignment.lower() == "top":
			top = self.p.margin[1]
			height = self.p.height
		else:
			top = self.p.margin[1]
			height = self.parent.container.h - (self.p.margin[1] + self.p.margin[3])
				
		if self.p.horizontal_alignment.lower() == "right":
			left = self.parent.container.w - (self.rect.w + self.p.margin[2])
			width = self.p.width
		elif self.p.horizontal_alignment.lower() == "left":
			left = self.p.margin[0]
			width = self.p.width
		else:
			left = self.p.margin[0]
			width = self.parent.container.w - (self.p.margin[0] + self.p.margin[2])
			
		height = max(0, height)
		width = max(0, width)
		
		self.rect = pygame.Rect(left, top, width, height)
		self.container = self.rect.move(self.parent.container.x, self.parent.container.y)
		self.container = self.container.inflate(self.p.border_width * -2, self.p.border_width * -2)
		self.update_surface()
	
	def update_position(self,*args):
		self.update_self_position(self,*args)
		for child in self.get_childs():
			child.update_position()
	
	def update_surface(self):
		self.surface_content = self.f.render(self.content, True, self.p.color_content)
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA | pygame.HWSURFACE)
		#self.image.fill(self.p.background_color)
		self.image.fill(self.p.background_color)
		center = list(self.image.get_rect().center)
		if self.p.background_image:
			self.image.blit(getImage(self.p.background_image), getImage(self.p.background_image).get_rect(center=center))
		if self.p.border_width:
			#pygame.draw.rect(self.image, self.p.border_color, self.image.get_rect().inflate(-1*self.p.border_width, -1*self.p.border_width), self.p.border_width)
			self.image.fill(self.p.border_color, pygame.Rect(0, 0, self.p.border_width, self.rect.h))    #left
			self.image.fill(self.p.border_color, pygame.Rect(0, 0, self.rect.w, self.p.border_width)) #top
			self.image.fill(self.p.border_color, pygame.Rect(self.rect.w - self.p.border_width, 0, self.p.border_width, self.rect.h))
			self.image.fill(self.p.border_color, pygame.Rect(0, self.rect.h - self.p.border_width, self.rect.w, self.p.border_width))
		if self.p.text_align == "left":
			center[0] = self.surface_content.get_rect().center[0]
		elif self.p.text_align == "righr":
			center[0] = self.rect.w - self.surface_content.get_rect().center[0]
			
		if self.p.text_align == "top":
			center[1] = self.surface_content.get_rect().center[1]
		elif self.p.text_align == "bottom":
			center[1] = self.rect.h - self.surface_content.get_rect().center[1]
			
		center = center[0] + self.p.text_offset_x, center[1] + self.p.text_offset_y
		self.image.blit(self.surface_content, self.surface_content.get_rect(center=center))
		
				
	def move(self, rel):
		self.rect.move_ip(rel)
		self.container.move_ip(rel)
		
	def update(self):
		video = core.core.video.get_screen()
		rect = self.parent.container.clip(video.get_rect())
		if rect.w == 0: rect = pygame.Rect(0,0,0,0)
		video.subsurface(rect).blit(self.image, self.rect)
		for child in self.get_childs():
			child.update()
		