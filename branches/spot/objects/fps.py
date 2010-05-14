#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygame
import div
from library import core

class fps (div.div):
	def __init__(self, parent, *args, **kws):
		div.div.__init__(self, parent, *args, **kws)
		self.fps = [0]*500
		self.i = 0

	def update(self, *args, **kws):
		fps = core.core.clock.get_fps()
		self.fps[self.i] = fps
		self.i += 1
		self.i %= len(self.fps)
		if self.fps[-1]:
			self.content = "%s:%s" % ( int(sum(self.fps, 0) / len(self.fps)), self)
		else:
			self.content = "%s:%s" % ( "Avg", self)
		self.update_position()
		div.div.update(self)
	
	def __str__(self):
		return "%3d" % core.core.clock.get_fps()
