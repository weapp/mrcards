#!/usr/bin/python
import pygame
import sys
from gamezone import pint
import deck
import gamezone

def main():

    #self.game.show()
    
    
    game=gamezone.gamezone(caption="pruebas")#declaramos la zona de juegos y le anyadimos los jugadores y el mazo para robar
    
    
    game.add_player(id_deck="jug1")
    game.add_player(id_deck="jug2")
    game.add_player(id_deck="jug3")
    game.add_player(id_deck="jug4")
    
    game.add_player(id_deck="jug1")
    game.add_player(id_deck="jug2")
    game.add_player(id_deck="jug3")
    game.add_player(id_deck="jug4")
    
    game.add_playzone(id_deck="mesa",visible=True)
    
    
    def points_tute(number,suit):
        r=0
        if number=="As":
            r=11
        elif number==3:
            r=10
        elif number=="J":
            r=2
        elif number=="Q":
            r=3
        elif number=="K":
            r=4
        return r
            
    game.add_deckdraw(id_deck="Mazo para robar", cards=[["As",2,3,4,5,6,7,8,9,10,"J","Q","K"],["espadas","oros","bastos","copas"]],visible=False,point=points_tute)
    
    game.deckdraws[0].shuffle()
    
    game.draw_a_card() #robar una carta
    game.deal(4) #repartir cartas   
    
    print game
    
    down_func={
            pygame.K_DOWN   :   [pygame.display.toggle_fullscreen,[]] , \
            pygame.K_SPACE  :   [pint,{"x":"espacio","y":"pulsado"}] , \
            pygame.K_UP     :   [pint,("up","pulsado")] , \
            pygame.K_LEFT   :   [pint,[["left","pulsado"]]] , \
            pygame.K_RIGHT  :   [pint,["right"]], \
            pygame.K_k      :   pint, \
            pygame.K_ESCAPE :   sys.exit, \
            pygame.K_F5     :   game.show, \
            pygame.K_1      :   [game.seleccionar,0], \
            pygame.K_2      :   [game.seleccionar,1], \
            pygame.K_3      :   [game.seleccionar,2], \
            pygame.K_4      :   [game.seleccionar,3], \
            pygame.K_5      :   [game.seleccionar,4], \
            pygame.K_6      :   [game.seleccionar,5], \
            pygame.K_7      :   [game.seleccionar,6], \
            pygame.K_8      :   [game.seleccionar,7], \
            pygame.K_9      :   [game.seleccionar,8], \
            pygame.K_0      :   [game.seleccionar,9], \
            pygame.K_z      :   game.clear_selection, \
            pygame.K_t      :   game.throw_cards, \
            pygame.K_RETURN :   game.throw_cards, \
            pygame.K_e      :   game.end_turn, \
            pygame.K_s      :   game.sort_by_suit, \
            pygame.K_n      :   game.sort_by_number, \
            pygame.K_p      :   game.sort_by_points, \
            pygame.K_d      :   game.draw_a_card, \
    }
    
    game.set_down_func(down_func)
    
    game.show()   
    
    game.init_bucle()
    
    
    

if __name__ == "__main__": main()
