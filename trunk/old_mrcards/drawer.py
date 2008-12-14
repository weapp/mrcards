import pygame
import os
import sys
from math import sin, cos, pi, atan2, degrees
import random
from pickle import load, dump
from library import core

#dump(pars, open('/tmp/mrcards.dump', 'w'))
pars = {'theme':'default','rules':'culo','players':'player 1,player 2,player 3,player 4'}
try:
    pars2 = load(open('/tmp/mrcards.dump', 'rb'))
    for key in pars2.keys():
        pars[key]=pars2[key]
except:pass

print "\n",__file__,":\ncargado pars:",pars,"\n"


class Zones:
    def __init__(self):
        self.counter=0
        self.zones={}
    
    def create_color(self,item):
        self.counter+=1
        self.zones[self.counter]=item
        return (self.counter,self.counter,self.counter)
        
        
    def __getitem__(self, item):
        return self.zones[item]
        
    def clear(self):
        self.counter=0
        self.zones={}

class Property:
    def __init__(self):
        self.dict = {}
    
    def __getitem__(self, item):
        return self.dict[self.fun(item)]
    
    def __setitem__(self, item, value):
        self.dict[self.fun(item)] = value
    
    def has_key(self, key):
        return self.dict.has_key(self.fun(key))
        
    def fun(self,item):
        return id(item)
        
    def clear(self):
        self.dict = {}
       
class Propieties:
    def __init__(self):
        self.random = Property()
        self.position = Property()
        self.normal = Property()
        self.align = Property()
        self.image = {}
        self.card = {}        
                
    def clear(self):
        self.position.clear()
        self.normal.clear()
        self.align.clear()
    
class Drawer:
    def __init__(self, gamezone, caption="Untitled"):
    
        self.ancho = 50
        self.alto = 80
        self.props = Propieties()
        self.zones = Zones()
        
        # Inicializacion
        pygame.init()
        # pantalla a 640x480
        self.screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF | pygame.HWSURFACE |  pygame.RESIZABLE )
        # relog para controlar los frames por segundo
        # se asigna el nombre de la ventana
        
        pygame.display.set_caption(caption)
        
        self.gz=gamezone
        
        self.theme=pars["theme"]
        self.theme=os.path.join('themes', self.theme )
        
        self.screen=pygame.display.get_surface()
        self.fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( self.theme , 'tapete.png') ) )
        
        # Esto hace falta para acelerar las cosas, hay que convertir las imagenes
        self.fondo = self.fondo.convert()
        self.fondo_rect = self.fondo.get_rect()
        self.fondo_rect.left, self.fondo_rect.top = 0, 0.
        fondo=pygame.transform.scale(self.fondo, self.screen.get_size())
        self.screen.blit(fondo, self.fondo_rect)
        
        #m=menu.Menu( (None, "Cargando...", None) )
        #m.update()
        
        pygame.font.init
        #self.font=pygame.font.Font(pygame.font.get_default_font(), 30)
        self.font = pygame.font.Font( os.path.join(os.path.dirname(sys.argv[0]), "joinpd.ttf" ), 30)
        text=self.font.render("Cargando...", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect())
        
        #self.font=pygame.font.Font(pygame.font.get_default_font(), 12)
        #self.font = pygame.font.Font( os.path.join(os.path.dirname(sys.argv[0]), "joinpd.ttf" ), 12)
        
        

            
    def place_in_circle(self, list_, radio=0.5, center=None, start=0.75, clockwise_direction=True):
        if center == None:
            center = self.screen.get_rect().center
        length = len(list_)
        for n in range(length):
            if clockwise_direction: #declaramos count que determina por que punto de la circuferencia vamos
                count = - start - (n / float(length))
            else:
                count = start + (n / float(length))
            x = cos(count * 2 * pi)
            y = sin(count * 2 * pi)
            
            self.props.normal[list_[n]] = [x, y]
            self.props.position[list_[n]] = [self.screen.get_width() * (0.5 + radio * x), self.screen.get_height() * (0.5 + radio * y)]

            #pygame.draw.circle(self.screen, (prop(n, length, 255),prop(n, length, 255), 128), (list_[n].position[0], list_[n].position[1]), 15)
            #pygame.draw.circle(self.screen, (prop(n, length, 255), 128, prop(n, length, 255)), (list_[n].position[0] -10 * x, list_[n].position[1]-10 * y), 10)

    def place_in_line(self, list_, center=None, margin=False, normal=[0, 1]):
        if center == None:
            center = self.screen.get_rect().center
        length = len(list_)
        
        if margin:
            margintmp = float(margin)
        else:
            margintmp = float(self.ancho)
        
        for n in range(length):
            x, y = normal
            
            
            margin = [0, 0]
            margin[0] = margintmp * y
            margin[1] = margintmp * x

            self.props.normal[list_[n]]=[x, y]
            self.props.position[list_[n]]=[center[0] - margin[0] * (length - 1) / 2.0 + n * margin[0], center[1] + margin[1] * (length - 1) / 2.0 - n * margin[1]]
            
            #pygame.draw.circle(self.screen, (255, 255, 128), (list_[n].position[0], list_[n].position[1]), 8)
            #pygame.draw.circle(self.screen, (prop(n, length, 255), 128,prop(n, length, 255)), (list_[n].position[0] -10 * x, list_[n].position[1]-10 * y), 4)
            
    def place_in_random(self, list_, center=None, margin=False, normal=[0, 1]):
        if center == None:
            center = self.screen.get_rect().center
        if margin:
            margintmp = float(margin)
        else:
            margintmp = float(self.ancho)
        margin=margintmp
        length = len(list_)
        
        for n in range(length):
            if not self.props.random.has_key(list_[n]):
                self.props.random[list_[n]] = [random.random(), (random.random() * 2 - 1), (random.random() * 2 - 1)]
            rand = self.props.random[list_[n]]

            x = cos(rand[0] * 2 * pi)
            y = sin(rand[0] * 2 * pi)
            
            self.props.normal[list_[n]] = [x, y]
            self.props.position[list_[n]] = [center[0] + rand[1] * margin, center[1] + rand[2] * margin]
            
            #pygame.draw.circle(self.screen, (255, 255, 128), (list_[n].position[0], list_[n].position[1]), 8)
            #pygame.draw.circle(self.screen, (prop(n, length, 255), 128,prop(n, length, 255)), (list_[n].position[0] -10 * x, list_[n].position[1]-10 * y), 5)
    
        
    
    def align(self, obj, align_vertical="center"):
            if align_vertical == "bottom":
                self.props.position[obj][0]-=self.props.normal[obj][0]*self.alto/2.0
                self.props.position[obj][1]-=self.props.normal[obj][1]*self.alto/2.0
            elif align_vertical == "center":
                pass
            elif align_vertical == "top":
                self.props.position[obj][0]+=self.props.normal[obj][0]*self.alto/2.0
                self.props.position[obj][1]+=self.props.normal[obj][1]*self.alto/2.0
                  
    def show(self):
        self.props.clear()
        self.zones.clear()
        
        self.core=core.Core()
        self.app=self.core.get_app()
        
        self.playersnames=[]
        for player in self.app.m['players']:
            self.playersnames.append(player.id)
    
        size = self.screen.get_size()
        
        #crear una surface alternativa donde se colocara los indices de cada carta
        self.alt_screen=pygame.Surface(size)
        
        #esto sirve para cuando se cambia el tamanyo de la ventena
        fondo = pygame.transform.scale(self.fondo, size)
        self.screen.blit(fondo, self.fondo_rect)

        #pintar comandos
        '''text = self.font.render(nself.gz.keys_descriptions, True, (255, 255, 255))
        self.screen.blit(text, text.get_rect())'''
        
        #mostrar los nombres de los jugadores
        self.place_in_circle(self.playersnames)
        for player in self.playersnames:
            self.align(player,align_vertical="bottom")
            self.align(player,align_vertical="bottom")
            self.align(player,align_vertical="bottom")
        for player in self.playersnames:
            self.show_text(player)
        
        #situamos los mazos
        self.place_in_circle(self.app.m['players'])
        self.place_in_circle(self.app.m['deckdraws'], radio=0.25, \
                            start=0.75 - 1.0 / len(self.app.m['players']) / 2 )
        self.place_in_circle(self.app.m['playzone'], radio=0)
        
        #alineamos las mazos
        for deck in self.app.m['players']:
            self.align(deck,align_vertical="bottom")
        for deck in self.app.m['deckdraws']:
            self.align(deck,align_vertical="center")
        for deck in self.app.m['playzone']:
            self.align(deck,align_vertical="center")
            
        #situamos cartas
        for deck in self.app.m['players']:
            self.place_in_line(deck, center=self.props.position[deck], \
                               normal=self.props.normal[deck])
        for deck in self.app.m['deckdraws']:
            self.place_in_line(deck, center=self.props.position[deck], \
                               normal=self.props.normal[deck], margin=1)
        for deck in self.app.m['playzone']:
            self.place_in_random(deck, center=self.props.position[deck], \
                                 normal=self.props.normal[deck], margin=35)
        
        #pintamos las cartas
        list_of_decks = [self.app.m['players'], self.app.m['deckdraws'], self.app.m['playzone'], self.app.m['deckdiscard'], self.app.m['deckpoints']]
        
        for decks in list_of_decks:
            for deck in decks:
                for card in deck:
                    self.show_card(card)
        

        #situamos tiradas            
        self.place_in_line(self.gz.throws,normal=[1,0],center=[self.screen.get_size()[0]-self.alto*2.2,self.screen.get_size()[1]/2],margin=self.alto/2)
        #situamos cartas
        for throw in self.gz.throws:
            self.place_in_line(throw, center=self.props.position[throw], normal=[0,1],margin=self.ancho/2)
        #pintamos las cartas
        for deck in self.gz.throws:
            for card in deck:
                self.show_card(card, zoom=0.50)
        
        
        
        if self.gz.show_layer_alternative:
            self.screen.blit(self.alt_screen, self.screen.get_rect())
        
        #actualizamos la pantalla
        pygame.display.flip()
    
    def show_card(self, card, zoom=1):
        if card.selected:
            self.props.position[card][0] -= 20 * self.props.normal[card][0]
            self.props.position[card][1] -= 20 * self.props.normal[card][1]
        
        if card.visible:
            image = self.card_complete(card)

            if card.selected:
                pass #image.blit(self.image_card("selected"), (0, 0, 80, 80))

        else:
            image = self.image_card("c")
        
        
        
        image=pygame.transform.rotozoom(image, degrees(atan2(*self.props.normal[card])) , zoom )
        rect = image.get_rect()
        rect.center = self.props.position[card]
        self.screen.blit(image, rect)
        
        
        #anyadiendo al mapa de zonas
        color_zone=self.zones.create_color(card)
        surf=pygame.Surface([self.ancho,self.alto])
        pygame.draw.rect(surf, color_zone , (0,0,self.ancho,self.alto))
        
        surf=pygame.transform.rotozoom(surf, degrees(atan2(*self.props.normal[card])) , zoom ) #misma funcion de la carta
        
        surf.set_colorkey((0,0,0))
        
        rect_surf=surf.get_rect()
        rect_surf.center=rect.center
        
        self.alt_screen.blit(surf, rect_surf)
        
    def show_text(self, text, zoom=False):
        image = self.font.render(text, True, (0,0,0))
        image=pygame.transform.rotate(image, degrees(atan2(*self.props.normal[text])) )
        rect = image.get_rect()
        rect.center = self.props.position[text]
        self.screen.blit(image, rect)
        
    def card_complete(self,card):
        name=str(card.suit)+","+str(card.number) 
        if not self.props.image.has_key(name):
            image = self.image_card(card.suit)
            image.blit(self.image_card(card.number), (0, 0, 80, 80))
            self.props.card[name]=image
        return self.props.card[name].copy()
            
    def image_card(self,name):
        if not self.props.image.has_key(name):
            self.props.image[name] = pygame.image.load(os.path.join(os.path.dirname(sys.argv[0]), os.path.join( self.theme , str(name)+'.png') ) ).convert_alpha()
        return self.props.image[name].copy()
        
    def obtain_zone(self, (x, y)):
        color=self.alt_screen.get_at((x,y))
        if color[0]:
            r=self.zones[color[0]]
            print r
            return r
        else:
            print None
            return 0

def prop(i, max1, max2):
    return (i * max2) / float(max1)
    
    
