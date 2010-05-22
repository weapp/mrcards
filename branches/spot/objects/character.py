from library.stdmodules import module
from library import core
from library import ph2d
import pygame
import random
from library.resources import animation

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
    def __init__(self, parent, filename, num, up, down, left, right,  jump):
        module.Module.__init__(self)
        ph2d.Ph2D.__init__(self)
        self.animation = VxCharset(filename, int(num))        
        self.spr = pygame.sprite.Sprite()
        self.spr.image = self.animation.get_tile(0,0,0)
        self.spr.rect = self.spr.image.get_rect()
        self.g = pygame.sprite.GroupSingle()
        self.g.add(self.spr)
        
        core.core.event.keydown[jump].bind(self.jump)
        core.core.event.keypress[up].bind(self.go_up, self.not_go_up)
        core.core.event.keypress[down].bind(self.go_down, self.not_go_down)
        core.core.event.keypress[left].bind(self.go_left, self.not_go_left)
        core.core.event.keypress[right].bind(self.go_right, self.not_go_right)

        
        self.spr.rect.move_ip(random.gauss(50, 20),random.gauss(50, 20))
		
    def update(self):
        ph2d.Ph2D.update(self)
        self.spr.rect.move_ip(self.displacement)
        self.spr.image = self.animation.get_tile(self.veloc[0], self.veloc[1], self.velc_z )
        self.g.draw(core.core.video.get_screen())