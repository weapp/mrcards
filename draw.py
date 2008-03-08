import pygame
import os
import sys
from math import sin, cos,pi
import menu
import random

class draw:
    def __init__(self,gamezone,caption="Untitled",theme="default"):
        self.ancho=50
        self.alto=80
        
        self.playzone_cards={}
        
        # Inicializacion
        pygame.init()
        # pantalla a 640x480
        self.screen = pygame.display.set_mode((800,600), pygame.DOUBLEBUF | pygame.HWSURFACE |  pygame.RESIZABLE )
        # relog para controlar los frames por segundo
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
        
        #m=menu.Menu( (None, "Cargando...",None) )
        #m.update()
        
        pygame.font.init
        self.font=pygame.font.Font(pygame.font.get_default_font(),30)
        text=self.font.render("Cargando...",True,(255,255,255))
              
        self.screen.blit(text, text.get_rect())
        
        
        self.font=pygame.font.Font(pygame.font.get_default_font(),12)
        
        pygame.display.flip()
        for i in range (39):
            z=i**10*100+2500
            t=z-1**100**2000
            t=t-1**100**2000
            t=t-1**100**2000
            t=t-1**100**2000
            t=z-1**100**2000
            t=t-1**100**2000
            t=t-1**100**2000
            t=t-1**100**2000
        
    def show(self):
        size=self.screen.get_size()
        #esto sirve para cuando se cambia el tamanyo de la ventena
        fondo=pygame.transform.scale(self.fondo,size)
        self.screen.blit(fondo, self.fondo_rect)

        #pintar comandos
        text=self.font.render(self.gz.keys_decriptions,True,(255,255,255))
        self.screen.blit(text, text.get_rect())

        #pintamos los mazos
            
        position_deckdraws=(len(self.gz.players)-0.7)/len(self.gz.players)
        
        if len(self.gz.deckdraws)==1:
            self.show_deck(deck=self.gz.deckdraws[0],show_mode="circular",pars=(0.5,position_deckdraws,1,0))
        else:
            for i in range(len(gz.deckdraws)):
                self.show_deck(deck=self.gz.deckdraws[i],show_mode="circular",pars=(0.5,i/float(len(self.gz.deckdraws)),1,0))
            
        for i in range(len(self.gz.players)):
            self.show_deck(deck=self.gz.players[i],pars=(0.8,i/float(len(self.gz.players)), self.ancho,self.alto ) )
            
        self.show_deck(self.gz.playzone[0],show_mode=False,random_cards=True)
        
        #actualizamos la pantalla
        pygame.display.flip()
        
    def show_deck(self,deck,position=None,show_mode="circular",pars=None,random_cards=False):
        if position==None:
            position=self.screen.get_rect().center
            
            len_cards=len(deck.cards)
            
        if show_mode=="circular" and (not pars==None) and len(pars)==4:
            center=position
            r=pars[0] #radio                                                 ^
            n=pars[1] #(0,1) elem_actual/elem_totales  0: |   0.25: ->  0.5: |   0.75:<- 
                      #                                   V
            padding_width=pars[2]
            padding_height=pars[3]
            
            n_tmp=n
            n=(1.25-n)%1
            r=r/2.0
            
            #position al centro de donde se debe de colocar el mazo            
            position=[self.screen.get_width() * (0.5 + r*cos(n*2*pi)) , self.screen.get_height() * (0.5 + r*sin(n*2*pi)) ]
                        
                        
            pos=position[:]
            pos[0] -= (len_cards-1)*padding_width/2 * cos(n_tmp*2*pi)
            pos[1] += (len_cards-1)*padding_width/2 * sin(n_tmp*2*pi)
            
            for i in range(len_cards):
                position[0] = pos[0]+i*padding_width * cos(n_tmp*2*pi)
                position[1] = pos[1]-i*padding_width * sin(n_tmp*2*pi)
                self.show_card(deck.cards[i],position,n_tmp,random_cards)
        else:
            for i in range(len_cards):
                self.show_card(deck.cards[i],(position[0]-i,position[1]),random_cards=random_cards)

    def show_card(self,card,position=[0,0],n=0,random_cards=False):
        if position==None:
            position=self.screen.get_rect().center
            
        #si random : si no se ha pintado antes: guarda una posicion aleatoria
        #          :  en cualquier caso       : obtiene la posicion y pinta la carta
        if random_cards:
            if not self.playzone_cards.has_key(str(card)):
                self.playzone_cards[str(card)]=[random.random(),(random.random()*2-1)*35,(random.random()*2-1)*35]
                
            tmp=self.playzone_cards[str(card)]
            n=tmp[0]
            position=[position[0]+tmp[1] , position[1]+tmp[2]]
            
            
        theme=os.path.join('themes', self.theme )
        if card.visible:
            image = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,str(card.suit)+'.png') ) )
            image.blit(pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,str(card.number)+'.png') ) ),(0,0,80,80))
            if card.selected:
                image.blit(pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'selected.png') ) ),(0,0,80,80))


        else:
            image = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'c.png') ) )
        
        image=pygame.transform.rotate(image, 360*n)
        rect = image.get_rect()
        rect.center = position
        self.screen.blit(image, rect)
