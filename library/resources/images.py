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

"""
def load_image(file_name, colorkey=None):
  full_name = os.path.join('data', file_name)

  try:
    image = pygame.image.load(full_name)
  except pygame.error, message:
    print 'Cannot load image:', full_name
    raise SystemExit, message

  image = image.convert()

  if colorkey is not None:
    if colorkey is -1:
      colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)

  return image, image.get_rect()
"""
