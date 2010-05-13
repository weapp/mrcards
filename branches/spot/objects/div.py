from library.stdmodules import module
from library import core
import pygame
import re
from library.resources.images import getImage

class div(pygame.sprite.Sprite, module.Module):
	def __init__(self, parent=None, id=None, kind=None, content="", color_content="[0,0,0,0]", width="0", height="0", vertical_alignment="", \
				horizontal_alignment="", margin="[0,0,0,0]", background="[80,80,80,0]", background_image=None, \
				border_color="[0,0,0,0]", border_width="0", overflow="hidden",\
				font="DroidSans", font_size=12, bold="", underline="", italic="", text_align="center", vertical_align="center"\
				):
		module.Module.__init__(self, id, kind)
		pygame.sprite.Sprite.__init__(self)
		
		self.width = int(width)
		self.height = int(height)
		self.vertical_alignment = vertical_alignment
		self.horizontal_alignment = horizontal_alignment
		self.margin = map(int, re.match("\[(\d+),(\d+),(\d+),(\d+)\]",margin).groups())
		self.container = self.rect = pygame.Rect(0, 0, self.width , self.height)
		
		self.background = map(int, re.match("\[(\d+),(\d+),(\d+),(\d+)\]", background).groups())
		self.background_image = background_image
		
		self.border_color = map(int, re.match("\[(\d+),(\d+),(\d+),(\d+)\]", border_color).groups())
		self.border_width = int(border_width)

		self.content = content
		self.color_content = map(int, re.match("\[(\d+),(\d+),(\d+),(\d+)\]", color_content).groups())
		self.f = pygame.font.Font("data/"+font+".ttf", font_size)
		if bold: self.f.set_bold(1)
		if underline: self.f.set_underline(1)
		if italic: self.f.set_italic(1)
		self.surface_content = self.f.render(self.content, True, self.color_content)
		self.text_offset_x, self.text_offset_y = 0, 0
		self.text_align = text_align
		self.vertical_align = vertical_align
		
		self.update_position()
		self.set_parent(parent)
		self.update_position()
	

		
	def update_position(self,*args):
		if not self.parent is None:
			if self.vertical_alignment.lower() == "bottom":
				top = self.parent.container.h - (self.rect.h + self.margin[3])
				height = self.height
			elif self.vertical_alignment.lower() == "top":
				top = self.margin[1]
				height = self.height
			else:
				top = self.margin[1]
				height = self.parent.container.h - (self.margin[1] + self.margin[3])
					
			if self.horizontal_alignment.lower() == "right":
				left = self.parent.container.w - (self.rect.w + self.margin[2])
				width = self.width
			elif self.horizontal_alignment.lower() == "left":
				left = self.margin[0]
				width = self.width
			else:
				left = self.margin[0]
				width = self.parent.container.w - (self.margin[0] + self.margin[2])
				
			height = max(0, height)
			width = max(0, width)
			
			self.rect = pygame.Rect(left, top, width, height)
			self.container = self.rect.move(self.parent.container.x, self.parent.container.y)
			self.container = self.container.inflate(self.border_width * -2, self.border_width * -2)
			self.update_surface()
			
			for child in self.get_childs():
				child.update_position()
	
	def update_surface(self):
		self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA | pygame.HWSURFACE)
		#self.image.fill(self.background)
		pygame.draw.rect(self.image, self.background, self.image.get_rect().inflate(-self.border_width, -self.border_width))
		if self.border_width:
			pygame.draw.rect(self.image, self.border_color, self.image.get_rect().inflate(-self.border_width, -self.border_width), self.border_width)
				
		center = list(self.image.get_rect().center)
		
		if self.background_image:
			self.image.blit(getImage(self.background_image), getImage(self.background_image).get_rect(center=center))
		
		if self.text_align == "left":
			center[0] = self.surface_content.get_rect().center[0]
		elif self.text_align == "righr":
			center[0] = self.image.get_rect().w - self.surface_content.get_rect().center[0]
			
		if self.text_align == "top":
			center[1] = self.surface_content.get_rect().center[1]
		elif self.text_align == "bottom":
			center[1] = self.image.get_rect().h - self.surface_content.get_rect().center[1]
			
		center = center[0] + self.text_offset_x, center[1] + self.text_offset_y
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
		