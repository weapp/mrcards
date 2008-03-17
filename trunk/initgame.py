#!/usr/bin/python
import pygame
import sys
import deck
import gamezone




def main(rules,players):
    #self.gamezone.show()
    
    players=players.replace('_'," ").split(",")
    
    game=gamezone.Gamezone(rules=rules)#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
    actions=game.actions
    rules=game.rules
    
    for player in players:
        game.add_player(id_deck=player)
    
    if rules.playzone:
        game.add_playzone(id_deck="playzone",visible=True)
    
    for deck in rules.deckdraws:
        game.add_deckdraw(id_deck=deck["name"], cards=[deck["numbers"],deck["suits"]],visible=False,point=rules.points)
    
    rules.init()
    
    
    print game
    
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
