#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.stdmodules import module
import pygame

class ShowDic(module.Module, dict):
    def __init__(self, surface,**dic):
        self.update_dict(dic)
        self.surface = surface
        self.font = pygame.font.Font(None, 16)
        self.height_line = self.font.get_height()
    
    def draw(self):
        for i,kv in enumerate(self.items()):
            key,value=kv
            image = self.font.render(str(key) + ':', 1, (255, 100, 100))
            image2 = self.font.render('   '+str(value), 1, (100, 255, 100))
            rect = image.get_rect()
            rect2 = image2.get_rect()
            rect.move_ip(10, 40 + 2 * i * self.height_line)
            rect2.move_ip(10, 40 + (2 * i + 1) * self.height_line)
            self.surface.blit(image, rect)
            self.surface.blit(image2, rect2)
            
    def update_dict(self,dic):
        dict.update(self,dic)
