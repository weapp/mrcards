import pygame
from os import path

SKIN='../../game/images'
FORMAT = 'png'

cache={}


def cacheImage(name, force=False):
    if force or not cache.has_key(str(name)):
        cache[name] = loadImage(name)
        
        
def loadImage(name, force=False):
    #fullname = path.dirname(__file__) + path.sep +'..' + path.sep + 'images' + path.sep + name + '.png'
    fullname = path.dirname(__file__) + path.sep + SKIN + path.sep + str(name) + '.' + FORMAT
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image: ' + str(name)
        raise SystemExit, message
    return image.convert_alpha()

    
def getImage(name):
    cacheImage(name)
    return cache[str(name)]
