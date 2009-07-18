# -*- coding: utf-8 -*-
# Copyright 2006 Hugo Ruscitti <hugoruscitti@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

import pygame
from pygame.locals import *
import os


class Animation:
    "Permite controlar animaciones almacenadas en una grilla de cuadros"
    
    def __init__ (self, path, colorkey, rows, cols):
        "Genera una animacion en base a una grilla de cuadros"
        
        self.create_tiles (path, colorkey, rows, cols)
        self.index = 0
        self.step = 0
        self.flip = 0
        self.frames = [0]
        self.delay = 10
        self.counter_delay = 0
        self.dx = 0
        self.dy = 0

    def set_flip (self, new_flip):
        self.flip = new_flip

    def create_tiles (self, path, colorkey, rows, cols):
        "Genera dos listas con cuadros de animación 'recortando' una grilla"
        
        image, rect = self.load_image (path, colorkey)
        self.tiles = self.tile_image (image, rows, cols)
        self.flip_tiles = map (self.horizontal_flip, self.tiles)
        del image

    def get_rect (self):
        return self.tiles [0].get_rect ()

    def get_actual_frame (self, flip = 0):
        "Informa que cuadro debe ser mostrado"
        
        if flip:
            return self.flip_tiles [self.index]
        else:
            return self.tiles [self.index]

    def draw_frame (self, dst, index, x, y):
        "Imprime sobre 'dst' un cuadro de animacion arbitrario indicado por 'index'"
        
        dst.blit (self.tiles [index], (x, y))

    def horizontal_flip (self, s):
        "Genera una imagen 'espejo horizontal' a partir de 's'"
        return pygame.transform.flip (s, 1, 0)
    
    def set_frames (self, new_frames):
        "Define la secuencia de cuadros para la animación actual, por ejemplo [0, 1, 2]"
        
        self.frames = new_frames
        self.step = 0
        self.counter_delay = 0
        self.index = self.frames [0]
    
    def advance (self):
        "Avanza un cuadro de animación hacia adelante, retorna 1 si llegó al final de animación y se reinicia"
        
        if self.counter_delay < self.delay:
            self.counter_delay += 1
            return 0
        else:
            self.counter_delay = 0
            self.step += 1
            
            if self.step > len (self.frames) - 1:
                self.step = 0
                self.index = self.frames [self.step]
                return 1
            else:
                self.index = self.frames [self.step]
                return 0

    def tile_image (self, image, rows, cols):
        "Genera una lista con los cuadros de animación en una grilla"
    
        tile_w = image.get_width () / cols
        tile_h = image.get_height () / rows
        tiles = []
    
        for c in xrange (cols):
            for r in xrange (rows):
                rect = c * (tile_w - 1) + c , r * (tile_h - 1) , tile_w, tile_h
                tiles.append (image.subsurface(rect).copy ())
    
        return tiles
    
    def load_image (self, name, colorkey = None):
        "Carga una imagen generando una superficie"
        
        fullname = os.path.join ('data', name)
    
        try:
            image = pygame.image.load (fullname)
        except pygame.error, message:
            print "Cannot load image: ", fullname
            raise SystemExit, message
    
        if colorkey is not None:
            image = image.convert ()
            if colorkey is -1:
                colorkey = image.get_at ((0, 0))
        
            image.set_colorkey (colorkey, RLEACCEL)
        else:
            if image.get_alpha () is None:
                image = image.convert ()
            else:
                image = image.convert_alpha ()
    
        return image, image.get_rect ()