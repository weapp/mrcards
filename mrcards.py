#!/usr/bin/python

import sys
import pygame
import menu
from menu import dec 
import os
from pickle import load, dump

#dump(pars, open('/tmp/mrcards.dump', 'w'))
pars = {'theme':'default','rules':'culo'}
try:pars = load(open('/tmp/mrcards.dump', 'rb'))
except:pass
print "\n\n\ncargado pars:",pars

global pars

def main(options="mrcards"):
    mc=Mrcards(options)
    mc.init_bucle()
    
class Mrcards:
    def __init__(self,options="mrcards"):
        self.options=options
        mrcards=("Start Game","Select Game","Players","Select Theme","Credits")
        games=self.rules()
        themes=self.themes()
        
        options=eval(options)
        
        # Inicializacion
        pygame.init()
        # pantalla a 640x480
        scrn_anch=640
        scrn_alto=480
        self.screen=screen=pygame.display.set_mode((scrn_anch, scrn_alto), pygame.DOUBLEBUF | pygame.HWSURFACE)
        # se asigna el nombre de la ventana
        pygame.display.set_caption('Menu')

        


        #Definir menu
        self.obj_menu=menu.Menu(options,110,30,interlineado=8,nvisibles=7)
        
        self.theme=os.path.join('themes',pars['theme'])
        try:self.fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( self.theme ,'menu.png') ) ).convert()
        except:self.fondo = pygame.image.load( os.path.dirname(sys.argv[0])+os.sep+'themes'+os.sep+'default'+os.sep+'menu.png' ).convert()
        
        
        self.fondo=pygame.transform.scale(self.fondo, screen.get_size())
        
        self.update()
        self.obj_menu.update()

    def init_bucle(self):
        # reloj para controlar los frames por segundo
        clock = pygame.time.Clock()
        # Bucle principal
        while True:
            clock.tick(40)
                
            # control de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # si no es un evento de teclado o raton, lo ignoramos
                if not hasattr(event,'button') and not hasattr(event,'key'):
                    continue
                
                # Eventos de raton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print "boton" + str(event.button)
                # Eventos de teclado
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_SPACE or event.key== pygame.K_RETURN:
                        self.seleccionar(self.obj_menu.position)
                    if event.key == pygame.K_UP:
                        self.update()
                        self.obj_menu.up()
                    if event.key == pygame.K_DOWN:
                        self.update()
                        self.obj_menu.down()

                elif event.type == pygame.KEYUP:
                    pass
        
            # Refresco de pantalla
            pygame.display.flip()

    def rules(self):
        archivos=os.listdir( os.path.join(os.path.dirname(sys.argv[0]), "rules") )
        pys=[]
        for archivo in archivos:
            if archivo[-3:]==".py":
                pys.append(archivo[:-3])
        return pys
        
    def themes(self):
        ruta=os.path.join(os.path.dirname(sys.argv[0]), "themes")
        archivos=os.listdir( ruta )
        themes=[]
        for archivo in archivos:
            if os.path.isdir(os.path.join(os.path.dirname(sys.argv[0]), "themes")+ os.sep +archivo):
                themes.append(archivo)
        return themes

    def seleccionar(self,n):
        if self.options=="mrcards":
            if n==0:
                __import__("initgame").main(players="player1,player2,player3,player4",rules=pars["rules"])
            if n==1:
                __import__("mrcards").main("games")
            if n==3:
                __import__("mrcards").main("themes")
            if n==4:
                credits=menu.Menu(("Author:","Weapp","weap88@gmail.com"),395,410, \
                interlineado=3,letra=(20,dec("FFFFFF"),dec("FFFFFF")),color_selec=())
                credits.update()
                
        if self.options=="games":
            global pars
            pars['rules']=self.obj_menu.options[self.obj_menu.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            __import__("mrcards").main("mrcards")
            
        if self.options=="themes":
            global pars
            pars['theme']=self.obj_menu.options[self.obj_menu.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            __import__("mrcards").main("mrcards")
            
            
    def update(self):
        self.screen,self.fondo
        self.screen.blit(self.fondo, self.fondo.get_rect())

# Esto es para que lance el main cuando se ejecute el fichero
if __name__ == "__main__": main()
