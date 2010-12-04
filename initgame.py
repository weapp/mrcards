#!/usr/bin/python
import pygame
import sys
import deck
import gamezone
import net


def main(rules, players, online=False):
    if online:
        netobj = net.Net(options=False)
        netobj.init_net(juego='culo', jugadores=2)
        players = netobj.players
        rules = netobj.juego
        game=gamezone.Gamezone(rules=rules, netobj=netobj, players=players)#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
        game.user = netobj.me
        # TODO las cartas se reparten aleatoriamente, 
        # Hay que hacer algo para que los distintos jugadores tengan las 
        # jueguen con la misma baraja
    else:
        players=players.replace('_'," ").split(",")
        game=gamezone.Gamezone(rules=rules, players=players)#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
    rules=game.rules
    game.new_round()
    game.set_down_func(rules.down_func)
    game.show()
    game.init_bucle()
    
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
    main(**options)
