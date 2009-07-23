#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame

from general import singleton
from stdmodules.apps import basicapp

pygame.init()

#SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 860
#(640,480))#TODO cambiar (esta asi para que me entre en la pantalla
SIZE=map(lambda x:int(x/1.5) , pygame.display.list_modes()[0] )
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE
TICKS = 40 #40 frames por segundo

pygame.display.init()

class Core:
    """
    clase principal encargada de iniciar una ventana de pygame y ponerle
    titulo.
    Sigue el patron Singleton y por tanto si llamas al constructor, siempre
    te devolvera la misma instancia.
    """

    __metaclass__ = singleton.Singleton

    set_caption=pygame.display.set_caption
    set_repeat=pygame.key.set_repeat
    
    def __init__(self):
        self.__size=SIZE
        self.__running=False
        self.stopped=False
        self.clock = pygame.time.Clock()
		        
    def set_size(self, size):
        self.__size = size
        if hasattr(self,'_Core__screen'):
            self.__screen = pygame.display.set_mode(self.__size, FLAGS)

    def get_app(self):
        if not hasattr(self,'_Core__app'):
            self.__app = basicapp.BasicApp()
        return self.__app

    def set_app(self, app):
        if hasattr(self,'_Core__app'):
            del self.__app
        self.__app = app
    
    def get_screen(self):
        self.__make_screen()
        return self.__screen
    
    def __make_screen(self):
        if not hasattr(self,'_Core__screen'):
            self.__screen=pygame.display.set_mode(self.__size, FLAGS)
	
    def init_video(self):
        if not hasattr(self,'_Core__screen'):
            pygame.display.set_mode(self.__size, FLAGS)
        
               
    def pause(self):
        self.__running=False
		
    def stop(self):
        self.__running=False
        self.stopped=True
        
    def start(self): #TODO cambiar los ticks dar prioridad a los logicos
        self.stopped=False
        """
        Inicia el bucle. En cada paso se de manejar los ticks y llama en cada
        paso a:
            app.new_event(event)
            app.update()
            app.draw()
            app.updated()
            y por ultimo actualiza la pantalla si asi lo dice app
        """
        self.__running=True
        while self.__running:
            self.clock.tick(TICKS)
            #control de eventos
            for event in pygame.event.get():
                if self.get_app().new_event(event):
                    continue
                if (event.type == pygame.KEYDOWN and \
                  event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    self.stop()
            #actualizado
            self.get_app().update()
            #pintado
            self.get_app().draw()
            if self.get_app().updated():
                self.__make_screen()
                pygame.display.flip()

        if self.stopped:
            del self.__app
            print "Parece que todo fue correctamente. :D"
        
    def change_scene(self,new):return self.set_app(new)
    def run(self):return self.start()


#esto es para que lance el main cuando se ejecute el fichero
if __name__ == "__main__":
    m=Core()
    m.start()
