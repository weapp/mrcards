import pygame
import sys
import os

#    font = pygame.font.SysFont("Akbar",30)
#    surfont = font.render("Eggs are good for you, but not on the eiffel tower",True,(0,255,255))
#    screen.blit(surfont, surfont.get_rect())

def dec(s):
    return (int(s[0:2], 16),int(s[2:4], 16),int(s[4:6], 16))


class Menu:
    def __init__(self,surface,options,margen_sup=0,margen_izq=0,interlineado=20,letra=(38,dec("5c3566"),dec("eff2f5")),color_base=(),color_selec=(213,213,213),menuEnBucle=True,only_text=False,nvisibles=7,persistant=False,seleccionar=None):
        self.surface=surface
        self.letra=letra
        self.options=options
        self.position=0
        self.margen_sup=margen_sup
        self.margen_izq=margen_izq
        self.interlineado=interlineado
        self.menuEnBucle=menuEnBucle
        self.nvisibles=nvisibles
        self.minvisible=0
        self.maxvisible=nvisibles
        self.optionvisibles=self.options[self.minvisible:self.maxvisible]
        
        self.color_base=color_base
        self.color_selec=color_selec
        
        #self.font = pygame.font.SysFont(letra[0],letra[1])
        self.font = pygame.font.Font( os.path.join(os.path.dirname(sys.argv[0]), "joinpd.ttf" ) , letra[0])
        self.surfont=[]
        self.ancho=0
        self.colorletra=(letra[1],letra[2])
        
        self.activate=persistant
        self.persistant=persistant
        
        self.editable=False
        
        if seleccionar: self.seleccionar=seleccionar
        
        for i in range(len(self.options)):
            self.surfont.append(self.font.render(self.options[i],True,letra[1]))
            if self.ancho<self.surfont[i].get_width():
                self.ancho=self.surfont[i].get_width() 
            
        self.alto=self.surfont[0].get_height()
    
    def no_out(self):
        #actuacion en caso de que se salga del array
        if self.menuEnBucle:
            self.position=self.position%len(self.options)
        else:
            if self.position < 0:
                self.position = 0
            elif self.position >= len(self.options):
                self.position = len(self.options)-1
                
        if self.position>=(self.maxvisible):
            self.minvisible=self.position-self.nvisibles+1
            self.maxvisible=self.position+1
            self.optionvisibles=self.options[self.minvisible:self.maxvisible]
            
        if self.position<=(self.minvisible):
            self.minvisible=self.position
            self.maxvisible=self.position+self.nvisibles
            self.optionvisibles=self.options[self.minvisible:self.maxvisible]
    
    def draw(self):
        #mostrar por terminal en que posicion "se enkuentra el cursor"
        try:
            r=str(self.position) + ": " + repr(self.options[self.position])
        finally:pass
           
        #pintar todos los rekuadros y el texto de las opciones
        
        for i in range(len(self.optionvisibles)):
            rect=(self.margen_izq-10, self.margen_sup+self.interlineado*i+self.alto*i-6, 350, self.alto+12)
            
            
            if i==self.position-self.minvisible:
                if len(self.color_selec):
                    #pygame.draw.rect(self.surface, self.color_selec, rect)
                    theme=os.path.join('themes', 'default' )
                    
                    try:select = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( theme ,'selectmenu.png') ) )
                    except:select = pygame.image.load( os.path.join(os.path.dirname(sys.argv[0]), os.path.join( 'default' ,'selectmenu.png') ) )
                    
                    self.surface.blit(select, rect)

                    
            else:
                if len(self.color_base):
                    pygame.draw.rect(self.surface, self.color_base, rect)
            
            rect=(self.margen_izq, self.margen_sup+self.interlineado*i+self.alto*i, self.ancho, self.alto)
                    
            if i==self.position-self.minvisible:
                self.surfont[i]=self.font.render(self.optionvisibles[i],True,self.colorletra[1])
            else:
                a=self.optionvisibles[i]
                self.surfont[i]=self.font.render(a,True,self.colorletra[0])

            self.surface.blit(self.surfont[i], rect)
    
        #pintar el rektangulo resaltado
        #pygame.draw.rect(self.surface, self.color_selec, (self.margen_izq,  self.margen_sup+self.interlineado*self.position+self.alto*self.position, self.ancho, self.alto))


    def update(self):
        self.optionvisibles=self.options[self.minvisible:self.maxvisible]
        
    def change_options(self,options):
        self.options=options
        self.position=0
        self.minvisible=0
        self.maxvisible=self.nvisibles
        self.optionvisibles=self.options[self.minvisible:self.maxvisible]
        self.surfont=[]
        for i in range(len(self.options)):
            self.surfont.append(self.font.render(self.options[i],True,self.letra[1]))
            if self.ancho<self.surfont[i].get_width():
                self.ancho=self.surfont[i].get_width() 
        
        
    def down(self):
        self.position+=1
        self.no_out()
        
    def up(self):
        self.position-=1
        self.no_out()
        
    def obtain_position(self):
        return self.position
        
    def editar(self,n):
        self.editable=True
        self.options[n]=''
        self.optioneditable=n
    
    def new_event(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.activate = not self.activate
                return True
            if self.activate or self.persistant:
                if self.editable:
                    if event.key== pygame.K_RETURN:
                        self.editable=False
                    elif event.key == pygame.K_SPACE:
                        self.options[self.optioneditable] += " "
                    elif event.key == pygame.K_BACKSPACE:
                        self.options[self.optioneditable] = self.options[self.optioneditable][:-1]
                    elif pygame.key.name(event.key) in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9","."]:
                        keyname = pygame.key.name(event.key)
                        
                        mod = pygame.key.get_mods()
                                                    
                        if mod in [pygame.KMOD_LSHIFT,pygame.KMOD_RSHIFT,pygame.KMOD_CAPS]:
                            self.options[self.optioneditable] += keyname.upper()
                        else:
                            self.options[self.optioneditable] += keyname
                        
                else:
                    if event.key == pygame.K_SPACE or event.key== pygame.K_RETURN:
                        self.seleccionar(self.position)
                    elif event.key == pygame.K_UP:
                        self.up()
                    elif event.key == pygame.K_DOWN:
                        self.down()
                return True
    
    def seleccionar(self,n):
        pass
