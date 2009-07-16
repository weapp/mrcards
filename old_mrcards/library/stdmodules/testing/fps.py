#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
from library.stdmodules import module

class Fps (module.Module):
    def __init__(self, surface, clock):
        self.surface = surface
        self.clock = clock
        self.font = pygame.font.Font(None, 16)

    def draw(self):
        self.image = self.font.render("FPS: %s" % self, 1, (255, 255, 100))
        self.surface.blit(self.image, self.image.get_rect().move(10,10))
        
    def __str__(self):
        return "%3d" % self.clock.get_fps()
