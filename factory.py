from library.stdmodules.controller import toogle_fullscreen as toogle_fullscreen_
from library.stdmodules.controller import bindingmanager
from library.stdmodules.menu.menu2 import Menu as Menu2
from library.stdmodules.testing import fps as fps_
from library.resources.images import getImage
from library.stdmodules.menu.menu import Menu
from library.stdmodules.apps import basicapp
from library.resources import animation
from library.stdmodules import module
from library import core
from library import ph2d

import library.stdmodules.sidebar as sidebar_
import pygame

def pos(x, y):
    return (int(x), int(y))

class background(basicapp.BasicApp):
    def __init__(self, filename):
        basicapp.BasicApp.__init__(self)
        self.spr = pygame.sprite.Sprite()
        self.spr.image = getImage(filename)
        self.spr.rect = self.spr.image.get_rect()
        self.g = pygame.sprite.GroupSingle()
        self.g.add(self.spr)
        
    def update(self):
        self.g.draw(core.core.video.get_screen())
        
class itemmenu(pygame.sprite.Sprite, module.Module):
    def __init__(self, name, func):
        module.Module.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        f = pygame.font.Font("font.ttf", 40)
        self.image = f.render(name, True, (255, 125, 0))
        self.image2 = f.render(name, True, (255, 200, 125))
        self.rect = self.image.get_rect()
        self.func = func
		
        
        self.bind( "hover", self.change, self.change)
        self.bind( "click", self.onclick)
    
    def change(self, *args):
        self.image, self.image2 = self.image2, self.image
    
    def onclick(self, *args):
        core.core.get_app()['SceneManager'].change_scene(self.func)
        
class menu(basicapp.BasicApp):
    def __init__(self, pos, *args):
        basicapp.BasicApp.__init__(self)
        self.g = pygame.sprite.Group()
        
        i = 0
        for elem in args:
            elem.rect.move_ip(pos)
            elem.rect.move_ip(0, 45*i)
            self.g.add(elem)
            i+=1
            
    def update(self):
        self.g.draw(core.core.video.get_screen())

class libmenu(Menu):
	def __init__(self, *options):
		Menu.__init__(self, core.core.video.get_screen(), options, 60, 20, 10)
		self.activate = True
		
	def update(self):
		Menu.update(self)
		Menu.draw(self)

#(self,surface,options,margen_sup=0,margen_izq=0,interlineado=20,letra=(38,dec("5c3566"),dec("eff2f5")),color_base=(),color_selec=(213,213,213),menuEnBucle=True,only_text=False,nvisibles=7,persistant=False,seleccionar=None)

class libmenu2(Menu2):
	def __init__(self, *options):
		Menu2.__init__(self, core.core.video.get_screen(), options, 130, 20, 10)
		self.activate = True


screen=core.core.video.get_screen()

def list(*arg): return arg
def character(): return character_.Character()
def toogle_fullscreen(): return toogle_fullscreen_.Toogle()
def fps(): return fps_.Fps(screen,core.core.clock)
   
binds = bindingmanager.BindingManager

def sidebar():
    rect = screen.get_rect()
    rect.w = 175/2
    sub = screen.subsurface(rect)
    return sidebar_.Sidebar(sub)


class VxCharset:
	def __init__(self, filename, num):
		self.index = 0
		self.animation = animation.Animation(filename, None, 8, 12)
		self.directions = {"down":0, "left":1, "right":2, "up":3}
		self.direction = self.directions["down"]
		self.sequence = [0,1,2,1]
		self.ratio = 10 #cada cuantos ticks se anima
		self.character= (0,4,24,28,48,52,72,76)[num]
		
	def get_tile(self, dx=0, dy=0, dz=0):
		return self.animation.tiles[self.get_direction(dx, dy, dz) + self.get_frame(dx, dy, dz) + self.character]
	
	def get_frame(self, dx, dy, dz):
		if (dx == 0 and dy == 0) or dz != 0:
			return 8
		else:			
			self.index = (self.index + 1) % (self.ratio * len(self.sequence))
			return self.sequence[(self.index / self.ratio) % len(self.sequence)] * 8
	
	def get_direction(self, dx, dy, dz):
		if not (dx == 0 and dy == 0):
			if dy > 0:
				self.direction = self.directions["down"]
			elif dy < 0:
				self.direction = self.directions["up"]
			elif dx > 0:
				self.direction = self.directions["right"]
			elif dx < 0:
				self.direction = self.directions["left"]
		return self.direction
		

class character(module.Module, ph2d.Ph2D):
	def __init__(self, filename, num, up, down, left, right,  jump):
		module.Module.__init__(self)
		ph2d.Ph2D.__init__(self)
		self.animation = VxCharset(filename, int(num))		
		self.spr = pygame.sprite.Sprite()
		self.spr.image = self.animation.get_tile(0,0,0)
		self.spr.rect = self.spr.image.get_rect()
		self.g = pygame.sprite.GroupSingle()
		self.g.add(self.spr)
		
		self.bind("keypress.%s" % up, self.go_up, self.not_go_up)
		self.bind("keypress.%s" % down, self.go_down, self.not_go_down)
		self.bind("keypress.%s" % left, self.go_left, self.not_go_left)
		self.bind("keypress.%s" % right, self.go_right, self.not_go_right)
		self.bind("keydown.%s" % jump, self.jump)
		
		def prin(x):print x
		#self.toggle("keydown.space", (lambda event: prin(1), lambda event: prin(2), lambda event: prin(3), lambda event: prin(4))      )
		self.bind("keydown.space", lambda event: prin(1))
		
		#def prin(x):print x
		#self.bind("keypress.space", lambda event: prin("blu"), lambda event: prin("blu2") )
		
	def update(self):
		ph2d.Ph2D.update(self)
		self.spr.rect.move_ip(self.displacement)
		self.spr.image = self.animation.get_tile(self.veloc[0], self.veloc[1], self.velc_z )
		self.g.draw(core.core.video.get_screen())
