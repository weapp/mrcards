import types
import pygame
from library.stdmodules import module

class Toogle(module.Module):
    def __init__(self) :
        pass
        
    def new_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t: pygame.display.toggle_fullscreen()
            #elif event.key == pygame.K_b:pygame.display.set_mode(pygame.display.list_modes()[3])
        return False
        
    def update(self):
        pass        
        
    def draw(self):
        pass
