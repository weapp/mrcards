#!/usr/bin/python

#obsoleto en siguientes versiones

import sys

import pygame

import deck
import gamezone
import net
from library import core
from game import gameapp
import rules

def inicializa(specific_rules,players,online):
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
        app=gameapp.GameApp()
        c=core.Core()
        c.set_app(app)

        #game.add(basicapp.BasicApp())
        #setattr(game,'add_player',game[0].add)
    return players,app

def main(specific_rules, players, online=False):
    players,game=inicializa(specific_rules,players,online)
    game.rules=rules.get_module(specific_rules).Game()

    for player in players:
        game.m['players'].append(deck.Deck(id_deck=player))

    if game.rules.playzone:
        game.sub_app['playzone'].append(deck.Deck(id_deck="playzone",visible=True))

    game.sub_app['gamezone'].new_round()

    game.sub_app['gamezone'].set_down_func(game.rules.down_func)

    game.sub_app['gamezone'].show()

    core.Core().start()

if __name__ == "__main__":
    options={
    "rules":"culo", \
    "players":"Player_1,Player_2,Player_3,Player_4"
    }
    for key in options.keys():
        for option in sys.argv:
            if option.startswith('--'+key+':'):
                options[key]=option[ (len(key)+3) :]
                print key , " >>> ",option[ (len(key)+2) :]
    options['specific_rules']=options['rules']
    del options['rules']
    main(**options)
