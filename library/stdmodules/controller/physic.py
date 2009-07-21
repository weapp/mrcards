#!/usr/bin/env python
#-*- coding:utf-8 -*-

from library.general import singleton
import time
import pygame
from library.general.structures import vector
from library.general.structures.vector import vector as Vector

FLAG_COLLIDABLE=0x1

class Physic (object):
    __metaclass__ = singleton.Singleton

    def __init__(self):
        self.gravity=Vector(0,0,0)
