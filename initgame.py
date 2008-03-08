#!/usr/bin/python
import pygame
import sys
from gamezone import pint
import deck
import gamezone

def main():

    #self.game.show()

    rules="culo"
    players="Player_1,Player_2,Player_3,Player_4"
    
    for option in sys.argv:
        if option.startswith('--game:'):
            rules=option[7:]
            print "Import >>> ",option[2:]
        elif option.startswith('--players:'):
            players=option[10:]
            print "players >>> ",option[2:]
    
    rules=__import__("rules/"+rules)

    game=gamezone.gamezone(caption=rules.caption,game_rules=rules)#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
    
    try: rules.register_gamezone(game)
    except: pass
    
    players=players.replace('_'," ").split(",")
    for player in players:
        game.add_player(id_deck=player)
    
    if rules.playzone:
        game.add_playzone(id_deck="playzone",visible=True)
    
    for deck in rules.deckdraws:
        game.add_deckdraw(id_deck=deck["name"], cards=[deck["numbers"],deck["suits"]],visible=False,point=rules.points)
    
    rules.init()
    
    
    print game
    
    game.set_down_func(eval(rules.down_func))
    
    game.show()
    
    game.init_bucle()
    
if __name__ == "__main__": main()
