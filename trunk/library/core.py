#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame

from general import singleton
from stdmodules.apps import basicapp
import threading 
import video
import event

import time

pygame.init()
pygame.display.init()

class Core:
    """
    clase principal encargada de iniciar una ventana de pygame y ponerle
    titulo.
    Sigue el patron Singleton y por tanto si llamas al constructor, siempre
    te devolvera la misma instancia.
    """
    __metaclass__ = singleton.Singleton
    video = video.Video()
    event = event.EventManager()
        
    set_caption = pygame.display.set_caption
    set_repeat = pygame.key.set_repeat
    
    def __init__(self):
        self.__running = False
        self.stopped = False
        self.clock  =  pygame.time.Clock()
        self.__app = None
        self.ticks = 40 #40 frames por segundo
        self.__time=time.time()
        self.delay = 0
        self.velocity = 10
        self.vdelay = 0
        self.ontick = event.Event("tick")
        
    def get_app(self):
        return self.__app

    def set_app(self, app):
        self.__app = app
               
    def pause(self):
        self.__running = False
        
    def stop(self):
        self.__running = False
        self.stopped = True
        
    def start(self): #TODO cambiar los ticks dar prioridad a los logicos
        """
        Inicia el bucle. En cada paso se de manejar los ticks y llama en cada
        paso a:
            app.new_event(event)
            app.update()
            app.draw()
            app.updated()
            y por ultimo actualiza la pantalla si asi lo dice app
        """
        self.stopped = False
        self.__running = True
        while self.__running:
            #actualizar relojes
            self.clock.tick(self.ticks)
            self.time = time.time()
            self.delay = self.time - self.__time
            self.vdelay = self.velocity * self.delay
            self.__time = self.time
            
            #control de eventos
            for event in pygame.event.get():
                if self.event.new_event(event):
                    continue
                if (event.type == pygame.KEYDOWN and \
                  event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    self.stop() #TODO cambiar al sistema de eventos
            #actualizado
            self.__app.update()
            #pintado
            self.__app.draw()
            if self.__app.updated():
                self.video.update()

        if self.stopped:
            del self.__app
            print "Parece que todo fue correctamente. :D"
            for trhead in threading.enumerate():
                if trhead.name == 'MainThread':
                     print #TODO terminar todos los threads abiertos
                 
    def run(self):return self.start()
    def init(self):return self.start()


core = Core()

get_app = core.get_app
set_app = core.set_app
pause = core.pause
stop = core.stop
start = core.start
run = core.run
init = core.init
set_size = core.video.set_size
set_caption = core.set_caption
set_repeat = core.set_repeat