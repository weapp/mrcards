#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
import div
from library import core

class fps (div.div):
	def __init__(self, parent, *args, **kws):
		div.div.__init__(self, parent, *args, **kws)

	def update(self, *args, **kws):
		self.content = str(self)
		self.p.color_content = "#000"
		self.p.bakcground_color = "#F00F"
		self.update_position()
		div.div.update(self)
	
	def __str__(self):
		return "%3d" % core.core.clock.get_fps()
