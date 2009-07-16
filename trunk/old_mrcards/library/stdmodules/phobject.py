#!/usr/bin/env python
#-*- coding:utf-8 -*-
from controller import physic
import module

class PhObject (module.Module):

    def __init__(self,vel=physic.Vector(0,0,0),pos=physic.Vector(0,0,0),acel=physic.Vector(0,0,0),mass=0,flags=0):
        self.__phgear=physic.Physic()
        self.acel=acel
        self.vel=vel
        self.pos=pos
        self.mass=mass
        self.flags=flags
        
    def move(self,x,y,z):
        self.pos+=physic.Vector(x,y,z)
        
    def update(self):
        self.vel+=self.acel
        self.pos+=self.vel
