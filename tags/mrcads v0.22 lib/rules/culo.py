import pygame
import sys
from library import core
import genericgame

c=core.Core()
from actions import Actions as actions
gamezone=c.get_app()['gamezone']

class Game(genericgame.Game):
    def __init__(self):
        self.gamezone=gamezone
        self.actions=actions
        self.throws=[]
        self.ai=AI()
        self.caption="Culo"
        self.decription="Game of Culo"
        self.playzone=True
        self.deckdraws=[{"name":"Mazo para robar","numbers":["As",2,3,4,5,6,7,"J","Q","K"],"suits":["spades","diamonds","clubs","hearts"]}]
        self.keys_descriptions="F5:Reload  Esc:Exit  Down:Toggle Fullscreen  D:Draw a card\n" + \
                              "[1-10]:Add to/Rem from Selection  Z:Clear Selection  T,Return:Throws \n" + \
                              "E:End Turn  S:Sort P:Pass Turn F1-4:Choose User  F12:None User"
        self.down_func={
            pygame.K_DOWN   :   ["pygame.display.toggle_fullscreen()","local"] , \
            pygame.K_ESCAPE :   ["self.actions.exit()","local"], \
            pygame.K_F5     :   ["self.actions.show()","local"], \
            pygame.K_UP     :   ["self.actions.showalt()","local"], \
            pygame.K_z      :   ["self.actions.clear_selection","global"], \
            pygame.K_t      :   ["self.actions.throw_cards","global"], \
            pygame.K_RETURN :   ["self.actions.throw_cards","global"], \
            pygame.K_e      :   ["self.actions.end_turn()","global"], \
            pygame.K_s      :   ["self.actions.sort('points')","local"], \
            pygame.K_d      :   ["self.actions.draw_a_card","global"], \
            pygame.K_p      :   ["self.actions.pass_turn","global"], \

            pygame.K_1       :   actions.prueba1, \
            pygame.K_2       :   actions.prueba2, \
            
            pygame.K_F1      :   actions.F1, \
            pygame.K_F2      :   actions.F2, \
            pygame.K_F3      :   actions.F3, \
            pygame.K_F4      :   actions.F4, \
            pygame.K_F12     :   actions.F12, \

        }
        

    def points(self,number,suit):
        if number=="As":
            r=14
        elif number=="J":
            r=11
        elif number=="Q":
            r=12
        elif number=="K":
            r=13
        else:
            r=number
        return r
        
    def init_game(self):
        print self.gamezone.deckdraws # no se han creado los mazos... esto deberia estar creado ya
        self.gamezone.deckdraws[0].shuffle()
        self.actions.deal(60) #repartir cartas    
        
    def pass_turn(self):
        if self.gamezone.pass_turns_counter==len(self.gamezone.players)-1:
            #dar el turno al jugador que tiro la ultima carta, no hace falta porque casualmente es el siguiente
            #self.gamezone.players.index( self.throws[len(self.throws)-1][0].previous_owner)
            
            self.actions.clear_playzone()
            del self.throws[:]

    def throw_cards(self,selection):
        self.actions.ending_turn()
        self.throws.append(selection)
            
    def throwable_selection(self,selection):
        #tiene que haber algo seleccionado
        if len(selection)==0:return False
        
        #obtenemos el numero y todos han de ser iguales
        number=selection[0].number
        for card in selection:
            if not card.number==number: return False
        
        #si se cumple lo anterior y no ha habido tiradas, cualquiera es valida
        if len(self.throws)==0:
            return True
        
        #si ya hay tiradas entonces tendran que comprobarse mas parametros 
        else:
            last_throw=self.throws[len(self.throws)-1]
            if len(selection)==len(last_throw):
                if selection[0].points>last_throw[0].points:
                    return True
            return False
            
        """
    def new_turn(self):
        if self.gamezone.player_with_turn>0:
            self.actions.sort_by_points()
                #last_throw=throws[len(throws)-1][0].number
                
                
                
                
            pygame.K_1      :   ["self.actions.select(0)","global"], \
            pygame.K_2      :   ["self.actions.select(1)","global"], \
            pygame.K_3      :   ["self.actions.select(2)","global"], \
            pygame.K_4      :   ["self.actions.select(3)","global"], \
            pygame.K_5      :   ["self.actions.select(4)","global"], \
            pygame.K_6      :   ["self.actions.select(5)","global"], \
            pygame.K_7      :   ["self.actions.select(6)","global"], \
            pygame.K_8      :   ["self.actions.select(7)","global"], \
            pygame.K_9      :   ["self.actions.select(8)","global"], \
            pygame.K_0      :   ["self.actions.select(9)","global"], \
            pygame.K_x      :   ["self.actions.select(10)","global"], \
            pygame.K_c      :   ["self.actions.select(11)","global"], \
            pygame.K_v      :   ["self.actions.select(12)","global"], \
            pygame.K_b      :   ["self.actions.select(13)","global"], \
            pygame.K_n      :   ["self.actions.select(14)","global"], \
            pygame.K_m      :   ["self.actions.select(15)","global"], \
            pygame.K_l      :   ["self.actions.select(16)","global"], \
            pygame.K_k      :   ["self.actions.select(17)","global"], \
            pygame.K_j      :   ["self.actions.select(18)","global"], \
            pygame.K_h      :   ["self.actions.select(19)","global"], \
            pygame.K_g      :   ["self.actions.select(20)","global"], \
            pygame.K_f      :   ["self.actions.select(21)","global"], \
                
                
                
                
       
        """


class AI:
    def __init__(self):
        pass
