from library import menu2
import os
import sys
from pars import pars
from pickle import load, dump
from library import core

class Menu(menu2.Menu):

    def __init__(self,opt,surf,*args,**kw):
        self.opt=opt
        
        self.menus={
        'mrcards': (_("Start Game"),_("Start Game Online"),_("Select Game"),_("Players"),_("Select Theme"),_("Credits")),
        'games':self.rules(),
        'themes': self.themes(),
        'onlineoptions': [_('Master'),_('Client')],
        'onlineoptionsmaster': [_('Back'),_('Server IP'),_('Server Port'),_('Nickname'),_('Number of Players'),_('Next')],
        'onlineoptionsclient': [_('Back'),_('Server IP'),_('Server Port'),_('Nickname'),_('Next')],
        'players': [_('Back'),_('Add Player'),_('Delete Player')]
        }
        self.menus['players'].extend(pars['players'].split(","))
        
        menu2.Menu.__init__(self,surf,self.menus[opt],*args,**kw)
        
    def rules(self):
        archivos=os.listdir( os.path.join(os.path.dirname(sys.argv[0]), "rules") )
        pys=[]
        for archivo in archivos:
            if archivo[-3:]==".py":
                pys.append(archivo[:-3])
        return pys
        
    def themes(self):
        archivos=os.listdir( os.path.join(os.path.dirname(sys.argv[0]), "themes") )
        themes=[]
        for archivo in archivos:
            if os.path.isdir(os.path.join(os.path.dirname(sys.argv[0]), "themes")+ os.sep +archivo):
                if not archivo.startswith("."):
                    themes.append(archivo)
        return themes
        
    def entrar_submenu(self,submenu):
        self.change_options(self.menus[submenu])
        self.opt=submenu
        
    def seleccionar(self,n):
        if self.opt=="mrcards":
            if n==0:
                core.Core().stop()
                #TODO borrar todos los datos del menu, convertir el juego en un modulo
                import initgame
                initgame.main(players=pars["players"],specific_rules=pars["rules"],online=False)
                
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
                credits=menu2.Menu(self.surface,(_("Author")+":","Weapp","weap88@gmail.com"),395,410, \
                interlineado=3,letra=(20,menu2.dec("FFFFFF"),menu2.dec("FFFFFF")),color_selec=())
                credits.update()
                
        elif self.opt=="games":
            pars['rules']=self.options[self.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            self.entrar_submenu('mrcards')
            
        elif self.opt=="themes":
            pars['theme']=self.options[self.position]
            dump(pars, open('/tmp/mrcards.dump', 'w'))
            print "\n\n\nguardado pars:",pars
            self.entrar_submenu('mrcards')
            #__import__("mrcards").main("mrcards")
            
        elif self.opt=="players":
            if n==0:
                pars['players']=','.join(self.menus['players'][3:])
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
            if n==0:
                self.entrar_submenu('onlineoptionsmaster')
            if n==1:
                self.entrar_submenu('onlineoptionsclient')
        elif self.opt=="onlineoptionsmaster":
            if n==0:
                self.entrar_submenu('mrcards')
                #__import__("mrcards").main("mrcards")
            elif 0<n and n<5:
                self.editar(n)
            elif n==5:
                #TODO borrar todos los datos del menu, convertir el juego en un modulo
                import initgame
                initgame.main(players=pars["players"],rules=pars["rules"],online=self.options[1:4])
                #print self.options[1:4]
