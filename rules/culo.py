import pygame
import sys

class AI:
    def __init__(self):
        pass

class Game:
    def __init__(self,gamezone,actions):
        self.gamezone=gamezone
        self.actions=actions
        self.throws=[]
        self.ai=AI()
        self.caption="Culo"
        self.playzone=True
        self.deckdraws=[{"name":"Mazo para robar","numbers":["As",2,3,4,5,6,7,"J","Q","K"],"suits":["espadas","oros","bastos","copas"]}]
        self.down_func={
            pygame.K_DOWN   :   [pygame.display.toggle_fullscreen,[]] , \
            pygame.K_ESCAPE :   actions.exit, \
            pygame.K_F5     :   actions.show, \
            pygame.K_1      :   [actions.select,0], \
            pygame.K_2      :   [actions.select,1], \
            pygame.K_3      :   [actions.select,2], \
            pygame.K_4      :   [actions.select,3], \
            pygame.K_5      :   [actions.select,4], \
            pygame.K_6      :   [actions.select,5], \
            pygame.K_7      :   [actions.select,6], \
            pygame.K_8      :   [actions.select,7], \
            pygame.K_9      :   [actions.select,8], \
            pygame.K_0      :   [actions.select,9], \
            pygame.K_x      :   [actions.select,10], \
            pygame.K_c      :   [actions.select,11], \
            pygame.K_v      :   [actions.select,12], \
            pygame.K_b      :   [actions.select,13], \
            pygame.K_n      :   [actions.select,14], \
            pygame.K_m      :   [actions.select,15], \
            pygame.K_l      :   [actions.select,16], \
            pygame.K_k      :   [actions.select,17], \
            pygame.K_j      :   [actions.select,18], \
            pygame.K_h      :   [actions.select,19], \
            pygame.K_g      :   [actions.select,20], \
            pygame.K_f      :   [actions.select,21], \
            pygame.K_z      :   actions.clear_selection, \
            pygame.K_t      :   actions.throw_cards, \
            pygame.K_RETURN :   actions.throw_cards, \
            pygame.K_e      :   actions.end_turn, \
            pygame.K_s      :   actions.sort_by_points, \
            pygame.K_d      :   actions.draw_a_card, \
            pygame.K_p      :   actions.pass_turn
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
        
    def init(self):
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
            

    def new_turn(self):
        print "----------->----------->-------------->.>"
        if self.gamezone.player_with_turn>0:
            self.actions.sort_by_points()
                #last_throw=throws[len(throws)-1][0].number
       
            
