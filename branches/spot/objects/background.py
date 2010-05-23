from library import core
from library.stdmodules.apps import basicapp
import pygame
from library.resources.images import getImage
import div

class background(div.div):
    def __init__(self, parent, filename):
		div.div.__init__(self, parent, background_image=filename)