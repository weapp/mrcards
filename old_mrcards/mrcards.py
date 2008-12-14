#!/usr/bin/python

import sys
import os
import gettext
import pdb

import pygame

from library import menu2 as menu
from game import main_menu,gameapp
from library import core
from pars import pars

gettext.install('mrcards', './mo/', unicode=1)

def main(options="mrcards"):
    c=core.Core()
    c.set_caption(_('Menu'))
    c.set_size((640,480))
    c.set_repeat(90,90)
    c.set_app(gameapp.GameApp())
    app=c.get_app()
    app.option = "menu"
    while app.option:
        if app.option=="menu":
            #c=core.Core(_('Menu'),size=(640,480))
            mc=MrcardsMenu(c.get_screen(),options)
            c.get_app().add('mc',mc)
            c.start()
            del mc
        elif app.option=="game":
            import initgame
            initgame.main(**app.options)


class MrcardsMenu:
    def __init__(self,surface,options="mrcards"):
        print "-->",globals().keys(),"<--"
        print "-->",dir(),"<--"
        print "-->", __builtins__.vars().keys() ,"<--"
        print "-->", vars().keys() ,"<--"
        self.surface=surface
        self.editable=False
        #Definir menu
        self.obj_menu=main_menu.Menu(options,self.surface,110,30,interlineado=8,nvisibles=7,persistant=True)
        self.theme=os.path.join('themes',pars['theme'])
        try:self.fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( self.theme ,'menu.png') ) ).convert()
        except:self.fondo = pygame.image.load( os.path.dirname(sys.argv[0])+os.sep+'themes'+os.sep+'default'+os.sep+'menu.png' ).convert()
        self.fondo=pygame.transform.scale(self.fondo, surface.get_size())
        self.update()
        self.obj_menu.update()
        self.kill_while = False

    def new_event(self,event):
        self.obj_menu.new_event(event)
        self.repeat=(90,90)
        # si no es un evento de teclado o raton, lo ignoramos
        if not hasattr(event,'button') and not hasattr(event,'key'):
            return None
        # Eventos de raton
        if event.type == pygame.MOUSEBUTTONDOWN:
            print _("button") + str(event.button)
        if event.type == pygame.KEYDOWN and self.editable and event.key== pygame.K_RETURN:
            self.editable=False

    def update(self):
        self.obj_menu.update()

    def draw(self):
        self.surface.blit(self.fondo, self.fondo.get_rect())
        self.obj_menu.draw()


# Esto es para que lance el main cuando se ejecute el fichero
if __name__ == "__main__": main()
