from library.stdmodules.menu import menu2
import os
import sys
from pars import pars
from pickle import load, dump
from library import core
from library.resources import images
import pygame

images.SKIN='../../themes/default'

class DefMenu:
    def __init__(self, dic):
        pass
        

class Menu(menu2.Menu):
    def __init__(self, opt, surf):
        self.fondo = pygame.transform.scale(images.loadImage('menu'), surf.get_size())
        self.opt=opt
        self.dir_themes=os.path.join(os.path.dirname(sys.argv[0]), "themes")
        self.dir_rules=os.path.join(os.path.dirname(sys.argv[0]), "rules")
        
        self.menus={
        'mrcards': (_("Start Game"), _("Start Game Online"), _("Select Game"), _("Players"), _("Select Theme"), _("Credits"), _("Exit")), 
        'games':self.rules(), 
        'themes': self.themes(), 
        'onlineoptions': [_('Master'), _('Client')], 
        'onlineoptionsmaster': [_('Back'), _('Server IP'), _('Server Port'), _('Nickname'), _('Number of Players'), _('Next')], 
        'onlineoptionsclient': [_('Back'), _('Server IP'), _('Server Port'), _('Nickname'), _('Next')], 
        'players': [_('Back'), _('Add Player'), _('Delete Player')]
        }
        self.menus['players'].extend(pars['players'].split(", "))
        menu2.Menu.__init__(self, surf, self.menus[opt], 110, 30, interlineado=8, nvisibles=7, persistant=True)
        
        
        
    def rules(self):
        archivos=os.listdir(self.dir_rules)
        pys=[]
        for archivo in archivos:
            if archivo[-3:]==".py":
                pys.append(archivo[:-3])
        return pys
        
    def themes(self):
        archivos=os.listdir(self.dir_themes)
        themes=[]
        for archivo in archivos:
            if os.path.isdir(os.path.join(os.path.dirname(sys.argv[0]), \
                                          "themes")+ os.sep +archivo):
                if not archivo.startswith("."):
                    themes.append(archivo)
        return themes
        
    def entrar_submenu(self, submenu):
        self.change_options(self.menus[submenu])
        self.opt=submenu
        
    def opcion_marcada(self,name):
        return self.menus[self.opt][self.position] == _(name)
        
    def seleccionar(self):
        n = self.position
        if self.opt=="mrcards":
            if self.opcion_marcada('Start Game'):
                c=core.Core()
                app=c.get_app()
                app.option="game"
                app.options={'players': pars["players"], 
                            'specific_rules': pars["rules"], 'online': False}
                c.pause()
                
            if n==1:
                self.entrar_submenu('onlineoptions')
            if n==2:
                self.entrar_submenu('games')
            if n==3:
                self.entrar_submenu('players')
            if n==4:
                self.entrar_submenu('themes')
            if n==5:
                #TODO los creditos desaparecen antes de aparecer
                FFFFFF=menu2.dec("FFFFFF")
                credits=menu2.Menu(self.surface, (_("Author")+":", \
                                   "Weapp", "weap88@gmail.com"), 395, 410, \
                                   interlineado=3, letra=(20, FFFFFF, FFFFFF),\
                                   color_selec=())
                credits.update()
            if n==6:
                c=core.Core()
                app=c.get_app()
                app.option=""
                c.stop()
                
        elif self.opt=="games":
            pars['rules']=self.options[self.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:", pars
            self.entrar_submenu('mrcards')
            
        elif self.opt=="themes":
            pars['theme']=self.options[self.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:", pars
            self.entrar_submenu('mrcards')
            #__import__("mrcards").main("mrcards")
            
        elif self.opt=="players":
            if n==0:
                pars['players']=', '.join(self.menus['players'][3:])
                dump(pars, open('/tmp/mrcards.dump', 'w'))
                self.entrar_submenu('mrcards')
                #__import__("mrcards").main("mrcards")
                
            if n==1:
                self.menus['players'].append('new_player')
                self.change_options(self.menus['players'])
                self.opt="players"
                
            if n==2:
                if len(self.menus['players'])>3:
                    del self.menus['players'][len(self.menus['players'])-1]
                self.change_options(self.menus['players'])
                self.opt="players"
            if n>2:
                self.editar(n)
                
        elif self.opt=="onlineoptions":
            if self.opcion_marcada('Master'):
                self.entrar_submenu('onlineoptionsmaster')
            if self.opcion_marcada('Client'):
                self.entrar_submenu('onlineoptionsclient')
        elif self.opt=="onlineoptionsmaster":
            if n==0:
                self.entrar_submenu('mrcards')
                #__import__("mrcards").main("mrcards")
            elif 0<n and n<5:
                self.editar(n)
            elif n==5:
                c=core.Core()
                app=c.get_app()
                app.option="game"
                app.options={'players': pars["players"], 
                            'specific_rules': pars["rules"], 'online': self.options[1:4]}
                c.pause()
                #print self.options[1:4]
                
    def draw(self):
        self.surface.blit(self.fondo, self.fondo.get_rect())
        menu2.Menu.draw(self)
