#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.stdmodules import module
from library.resources.images import getImage 
import pygame
from library import core
from pygame import Color
from library.resources import textrect
from HTMLParser import HTMLParser

pygame.font.init()
filename=pygame.font.match_font('Sans Serif')
font=pygame.font.Font(filename, 18)
antialias=True
right_margin=200

def formatear(string):
    string=strip_tags(string)
    return cortar_a(string,20)

def strip_tags(html):
     result = []
     parser = HTMLParser()
     parser.handle_data = result.append
     parser.feed(html)
     parser.close()
     return ''.join(result)

def cortar_a(string,num):
    s=''
    n=0
    for st in string:
        s+=st
        if st==' ':
            n=0
            continue
        n+=1
        n%=num
        if n==0:
            s+=' '
    return s



class Sidebar(module.Module):
    def __init__(self,surface):
        module.Module.__init__(self)
        self.surface=surface
        self.rect=self.surface.get_rect()
        self.background=getImage('bar_izq')
        #self.background=pygame.transform.scale(self.background,( self.background.get_width() *  self.surface.get_width() / self.surface.get_height() , self.surface.get_height() ))
        self.background=pygame.transform.scale(self.background,self.surface.get_size())
        self.need_update=[self.surface.get_rect()]
              
    def draw(self):
        self.surface.blit(self.background,self.rect)
        self.need_update=[]
    
    def render_text_sidebar(self,txts,h,init,paso):
        for counter, txt in enumerate(txts):
            #counter+=init
            
            position=init[0]+paso[0]*counter,init[1]+paso[1]*counter
            
            txt=formatear(txt)
            rect_text=self.rect.move(0,0)
            rect_text.h=h
            rect_text.topleft=position
            
            txt2=textrect.render_textrect(txt, font, rect_text, Color('#FFFFFF'), None ,1)
            self.surface.blit(txt2,rect_text)
        return self.rect,self.surface    

    def render_button_sidebar(self,buttons,init,paso):
        for counter, button in enumerate(buttons):
            position=init[0]+paso[0]*counter,init[1]+paso[1]*counter
            button.rect.center=position
            
            if button.state=='enable':
                pygame.draw.rect(self.surface, Color('#AAAAAAFF'), button.rect)
                pygame.draw.rect(self.surface, Color('#FFFFFFFF'), button.rect, 1)

            self.surface.blit(button.image,button.rect)
        return self.rect,self.surface    

class Button:
    def __init__(self,id,image,state='disable'):
        self.id=id
        self.image=image
        self.rect=self.image.get_rect()
        self.id=id
        self.state=state
