import pygame
import sys
import os

#    font = pygame.font.SysFont("Akbar",30)
#    surfont = font.render("Eggs are good for you, but not on the eiffel tower",True,(0,255,255))
#    screen.blit(surfont, surfont.get_rect())
class Menu:
    def __init__(self,options,margen_sup=0,margen_izq=0,interlineado=20,letra=("Akbar",90,(0,125,255),(0,225,255)),color_base=(),color_selec=(213,213,213),menuEnBucle=True):
        
        # Inicializacion
        pygame.init()
        # pantalla a 640x480
        scrn_anch=640
        scrn_alto=480
        self.screen = screen= pygame.display.set_mode((scrn_anch, scrn_alto), pygame.DOUBLEBUF | pygame.HWSURFACE)
        # se asigna el nombre de la ventana
        pygame.display.set_caption('Menu')
        
        theme=os.path.join('themes', 'default' )
        
        fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'tapete.png') ) ).convert()
        
        fondo=pygame.transform.scale(fondo, screen.get_size())
        screen.blit(fondo, fondo.get_rect())
        
        self.options=options
        self.position=0
        self.margen_sup=margen_sup
        self.margen_izq=margen_izq
        self.interlineado=interlineado
        self.screen=screen
        self.menuEnBucle=menuEnBucle
        
        self.color_base=color_base
        self.color_selec=color_selec
        
        self.font = pygame.font.SysFont(letra[0],letra[1])
        self.surfont=[]
        self.ancho=0
        self.colorletra=(letra[2],letra[3])
        
        
        for i in range(len(self.options)):
            self.surfont.append(self.font.render(self.options[i],True,letra[2]))
            if self.ancho<self.surfont[i].get_width():
                self.ancho=self.surfont[i].get_width() 
            
        self.alto=self.surfont[0].get_height()
        
    def update(self):
           

        theme=os.path.join('themes', 'default' )
        
        fondo = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'tapete.png') ) ).convert()
        
        fondo=pygame.transform.scale(fondo, self.screen.get_size())
        self.screen.blit(fondo, fondo.get_rect())

        #actuacion en caso de que se salga del array
        if self.menuEnBucle:
            self.position=self.position%len(self.options)
        else:
            if self.position < 0:
                self.position = 0
            elif self.position >= len(self.options):
                self.position = len(self.options)-1
                
        #mostrar por pantalla en que posicion "se enkuentra el cursor"
        print self.position , ": " , self.options[self.position]
            
        #pintar todos los rekuadros y el texto de las opciones
        for i in range(len(self.options)):
            rect=(self.margen_izq, self.margen_sup+self.interlineado*i+self.alto*i, self.ancho, self.alto)
            
            if i==self.position:
                pygame.draw.rect(self.screen, self.color_selec, rect)
                self.surfont[i]=self.font.render(self.options[i],True,self.colorletra[1])
            else:
                if len(self.color_base)==0:
                    self.surfont[i]=self.font.render(self.options[i],True,self.colorletra[0])
                else:
                    pygame.draw.rect(self.screen, self.color_base, rect)
                    self.surfont[i]=self.font.render(self.options[i],True,self.colorletra[0])

            self.screen.blit(self.surfont[i], rect)
    
        #pintar el rektangulo resaltado
        #pygame.draw.rect(self.screen, self.color_selec, (self.margen_izq,  self.margen_sup+self.interlineado*self.position+self.alto*self.position, self.ancho, self.alto))
        
    def down(self):
        self.position+=1
        self.update()
        
    def up(self):
        self.position-=1
        self.update()
        
    def obtain_position(self):
        return self.position
