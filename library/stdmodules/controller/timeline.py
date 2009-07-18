#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general import singleton
import time
import pygame

class Timeline (object):
    __metaclass__ = singleton.Singleton

    def __init__(self,):
        self.countdowns=[]
        #self.initial_time=time.time() #un float con la marca d tiempoa actual
        #time.localtime() devuelve una tupla
        #self.clock=time.clock tiempo desde que se inicio
    
    def get_actual_time(self):
        return time.time()
    
    def add_event(event,delay,times=-1):
        self.countdowns.append(Countdown(event,delay,times))
        return self.countdowns[-1]
    
    class Countdown (object):
    
        def __init__(self,event,delay,times):
            self.original_times=times
            self.delay=delay
            self.event=event
            self.restart()
            
        def time_to_event(self):
            self.end_time-time.time()
            
        def modify_time(delay):
            self.end_time+=delay
        
        def get_elapsed(self):
            return self.tiem.time()-self.initial_time        
        
        def pause(self):
            self.__is_paused=True
            self.__elpased=self.get_elapsed()
        
        def is_pause(self):
            return self.__is_paused
            
        def resume(self):
            if self.__is_paused:
                self.__is_paused=False
                self.initial_time=time.time()-self.__elapsed
                del self.__elapsed
            
        def restart(self):
            self.initial_time=time.time()
            self.end_time=self.inititaltime+self.delay
            self.__is_paused=False
            self.times=self.original_times
            
        def self.update():
            if times and not self.__is_paused:
                if self.end_time<time.time():
                    self.end_time=time.time()+self.delay
                    self.times=max(self.times-1,-1)
                    pygame.event.post(self.event)
