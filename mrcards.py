#!/usr/bin/python

import sys
import pygame
import menu
from menu import dec 
import os
from pickle import load, dump


#dump(pars, open('/tmp/mrcards.dump', 'w'))
pars = {'theme':'default','rules':'culo','players':'player 1,player 2,player 3,player 4'}
try:
    pars2 = load(open('/tmp/mrcards.dump', 'rb'))
    for key in pars2.keys():
        pars[key]=pars2[key]
except:pass

print "\n\n\ncargado pars:",pars


def main(options="mrcards"):
    mc=Mrcards(options)
    mc.init_bucle()
    
class Mrcards:
    def __init__(self,options="mrcards"):
        self.options=options
        self.mrcards=("Start Game","Select Game","Players","Select Theme","Credits")
        self.games=self.rules()
        self.themes=self.themes()
        self.players=['Volver','Anyadir Player','Eliminar Player']
        self.players.extend(iter(pars['players'].split(",")))
        options=eval('self.'+str(options))
        
        self.editable=False
        
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
        self.kill_while = False

    def init_bucle(self):
        # reloj para controlar los frames por segundo
        clock = pygame.time.Clock()
        # Bucle principal
        while True:
            clock.tick(40)
            if self.kill_while:
                break   
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
                    elif not self.editable:
                        if event.key == pygame.K_SPACE or event.key== pygame.K_RETURN:
                            self.seleccionar(self.obj_menu.position)
                        elif event.key == pygame.K_UP:
                            self.update()
                            self.obj_menu.up()
                        elif event.key == pygame.K_DOWN:
                            self.update()
                            self.obj_menu.down()
                    else:
                        if event.key== pygame.K_RETURN:
                            self.editable=False
                        elif event.key == pygame.K_SPACE:
                            self.obj_menu.options[self.optioneditable] += " "
                        elif event.key == pygame.K_BACKSPACE:
                            self.obj_menu.options[self.optioneditable] = self.obj_menu.options[self.optioneditable][:-1]
                            self.update()
                            self.obj_menu.update_options()
                        elif pygame.key.name(event.key) in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            keyname = pygame.key.name(event.key)
                            
                            mod = pygame.key.get_mods()
                                                        
                            if mod == pygame.KMOD_LSHIFT or mod == pygame.KMOD_RSHIFT or mod == pygame.KMOD_CAPS:
                                self.obj_menu.options[self.optioneditable] += keyname.upper()
                            else:
                                self.obj_menu.options[self.optioneditable] += keyname
                            self.update()
                            self.obj_menu.update_options()
                        
                            

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
                if not archivo.startswith("."):
                    themes.append(archivo)
        return themes

    def seleccionar(self,n):
        if self.options=="mrcards":
            if n==0:
                self.kill_while = True
                __import__("initgame").main(players=pars["players"],rules=pars["rules"])
            if n==1:
                #__import__("mrcards").main("games")
                self.obj_menu.change_options(self.games)
                self.options="games"
                self.update()
                self.obj_menu.update()
            if n==2:
                #__import__("mrcards").main("players")
                self.obj_menu.change_options(self.players)
                self.options="players"
                self.update()
                self.obj_menu.update()
            if n==3:
                self.obj_menu.change_options(self.themes)
                self.options="themes"
                self.update()
                self.obj_menu.update()
                #__import__("mrcards").main("themes")
            if n==4:
                credits=menu.Menu(("Author:","Weapp","weap88@gmail.com"),395,410, \
                interlineado=3,letra=(20,dec("FFFFFF"),dec("FFFFFF")),color_selec=())
                credits.update()
                
        elif self.options=="games":
            pars['rules']=self.obj_menu.options[self.obj_menu.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            self.obj_menu.change_options(self.mrcards)
            self.options="mrcards"
            self.update()
            self.obj_menu.update()
            #__import__("mrcards").main("mrcards")
            
        elif self.options=="themes":
            pars['theme']=self.obj_menu.options[self.obj_menu.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            __import__("mrcards").main("mrcards")
            
        elif self.options=="players":
            if n==0:
                pars['players']=','.join(self.players[3:])
                dump(pars, open('/tmp/mrcards.dump', 'w'))
                __import__("mrcards").main("mrcards")
                
            if n==1:
                self.players.append('new_player')
                self.obj_menu.change_options(self.players)
                self.options="players"
                self.update()
                self.obj_menu.update()
                
            if n==2:
                if len(self.players)>3:
                    del self.players[len(self.players)-1]
                self.obj_menu.change_options(self.players)
                self.options="players"
                self.update()
                self.obj_menu.update()
            if n>2:
                self.editable=True
                self.obj_menu.options[n]=''
                self.optioneditable=n
                self.obj_menu.update_options()
                self.update()
                self.obj_menu.update()
            
    def update(self):
        self.screen,self.fondo
        self.screen.blit(self.fondo, self.fondo.get_rect())

# Esto es para que lance el main cuando se ejecute el fichero
if __name__ == "__main__": main()
