import pygame
import os
import sys
from math import sin, cos,pi
import menu

class draw:
    def __init__(self,gamezone,caption="Untitled",theme="default"):
        self.ancho=50
        # Inicializacion
        pygame.init()
        # pantalla a 640x480
        self.screen = pygame.display.set_mode((800,600), pygame.DOUBLEBUF | pygame.HWSURFACE |  pygame.RESIZABLE )
        # relog para controlar los frames por segund
        # se asigna el nombre de la ventana
        
        pygame.display.set_caption(caption)
        
        self.gz=gamezone
        self.theme=theme
        self.screen=pygame.display.get_surface()
        
        theme=os.path.join('themes', theme )
        
        self.fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'tapete.png') ) )
        
        # Esto hace falta para acelerar las cosas, hay que convertir las imagenes
        self.fondo = self.fondo.convert()
        self.fondo_rect = self.fondo.get_rect()
        self.fondo_rect.left, self.fondo_rect.top = 0, 0.
        fondo=pygame.transform.scale(self.fondo, self.screen.get_size())
        self.screen.blit(fondo, self.fondo_rect)
        
        m=menu.Menu( (None, "Cargando...",None) )
        m.update()
        
        pygame.display.flip()
        
    def show(self):
        size=self.screen.get_size()
        fondo=pygame.transform.scale(self.fondo,size)
        self.screen.blit(fondo, self.fondo_rect)

        for deck in self.gz.deckdraws:
            self.show_deck(deck=deck,show_mode=None,pars=(0.5,0.85))
            
        for i in range(len(self.gz.players)):
            self.show_deck(deck=self.gz.players[i],pars=(0.8,i/float(len(self.gz.players))))
            
        pygame.display.flip()
        
    def show_deck(self,deck,position=None,show_mode="circular",pars=None):
        if position==None:
            position=self.screen.get_rect().center
            
            len_cards=len(deck.cards)
            
        if show_mode=="circular" and (not pars==None) and len(pars)==2:
            center=position
            r=pars[0] #radio                                                 ^
            n=pars[1] #(0,1) elem_actual/elem_totales  0: |   0.25: ->  0.5: |   0.75:<- 
                      #                                   V
            n_tmp=n
            n=(1.25-n)%1
            n=n*2*pi
            r=r/2.0
            position=[self.screen.get_width() * (0.5 + r*cos(n)) , self.screen.get_height() * (0.5 + r*sin(n)) ]
                        
            pos=position[:]
            pos=[pos[0]+len_cards*self.ancho/2,pos[1]]
            
            for i in range(len_cards):
                position[0]=pos[0]-i*self.ancho
                self.show_card(deck.cards[i],position,n_tmp)
        else:
            for i in range(len_cards):
                self.show_card(deck.cards[i],(position[0]-i,position[1]))

    def show_card(self,card,position=(0,0),n=0):
        if position==None:
            position=self.screen.get_rect().center
            
        image =  pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), 'c.png'))
        image=pygame.transform.rotate(image, 360*n)
        rect = image.get_rect()
        rect.center = position
        self.screen.blit(image, rect)
        
