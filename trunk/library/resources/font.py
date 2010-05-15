import pygame
from os import path

SKIN='data'
FORMATS = ['ttf']

cache={}


def cacheFont(name, size, force=False):
    if force or not (cache.has_key(str(name)) and cache[name].has_key(str(size))):
        cache.setdefault(str(name),{})[str(size)] = loadFont(name, size)
        
        
def loadFont(name, size, force=False): #TODO eliminar try y catch
    #fullname = path.dirname(__file__) + path.sep +'..' + path.sep + 'images' + path.sep + name + '.png'
    cargado = False
    for FORMAT in FORMATS:
        fullname = path.join (SKIN, str(name) + '.' + FORMAT)
        try:
            font = pygame.font.Font(fullname, size)
            cargado = True
            break
        except pygame.error, message:
            pass
    if not cargado:
        print 'Cannot load font: ' + str(name)
        raise SystemExit

    return font

def getFont(name, size):
    cacheFont(name, size)
    return cache[str(name)][str(size)]

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
