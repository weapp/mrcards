#!/usr/bin/python

import sys
import os
import gettext
import pdb

import pygame

from library.stdmodules.menu import menu2 as menu
from game import main_menu,gameapp
from library import core
from pars import pars
import deck
import gamezone
import net
import rules

gettext.install('mrcards', './mo/', unicode=1)

def main():
    c=core.Core()
    app = gameapp.GameApp()
    c.set_app(app)
    app.option = "menu"
    while app.option:
        if app.option=="menu":
            c.set_caption(_('Menu'))
            c.set_size((640,480))
            c.set_repeat(90,90)
            app.add('mc',main_menu.Menu('mrcards',c.get_screen()))
            c.start()
            del app['mc']
        elif app.option=="game":
            app.option=False
            specific_rules = app.options['specific_rules']
            players = app.options['players']
            online = app.options['online']
            
            if online:
                netobj = net.Net(options=False)
                netobj.init_net(juego='culo', jugadores=2)
                players = netobj.players
                specific_rules = netobj.juego
                game=gamezone.Gamezone(rules=specific_rules,netobj=netobj)#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
                game.user = netobj.me
                # TODO las cartas se reparten aleatoriamente,
                # Hay que hacer algo para que los distintos jugadores tengan las
                # jueguen con la misma baraja
            else:
                players=players.replace('_'," ").split(",")
                
            
            app.rules=rules.get_module(specific_rules).Game()

            for player in players:
                app.m['players'].append(deck.Deck(id_deck=player))

            if app.rules.playzone:
                app['playzone'].append(deck.Deck(id_deck="playzone",visible=True))

            app['gamezone'].new_round()

            app['gamezone'].set_down_func(app.rules.down_func)

            app['gamezone'].show()

            core.Core().start()
			
        else:
            app.option=False


# Esto es para que lance el main cuando se ejecute el fichero
if __name__ == "__main__": main()



"""
print "-->",globals().keys(),"<--"
print "-->",dir(),"<--"
print "-->", __builtins__.vars().keys() ,"<--"
print "-->", vars().keys() ,"<--"
"""
