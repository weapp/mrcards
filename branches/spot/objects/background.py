from library import core
from library.stdmodules.apps import basicapp
import pygame
from library.resources.images import getImage

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
