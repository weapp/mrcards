from library.stdmodules import module
from library.resources.images import getImage 
import pygame	

class Bg(module.Module):
    def __init__(self,surface,fondo,r=0,g=0,b=0):
        self.surface=surface
        self.background=getImage(fondo)
        self.background=pygame.transform.scale(self.background,( self.surface.get_width(), self.background.get_height() ))
        self.need_update=[self.surface.get_rect()]
        self.color=(r,g,b)
       
    def draw(self,rect=None):
        if not rect:
            rect=self.surface.get_rect()
        pygame.draw.rect(self.surface, self.color, rect)
        self.surface.blit(self.background, rect, rect)
        self.need_update=[]
