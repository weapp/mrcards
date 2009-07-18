#!/usr/bin/env python
#-*- coding:utf-8 -*-

from rules import genericgame
from library import core
import pygame
import sys

class AI:
    def __init__(self):
        pass

class Game(genericgame.Game):
    def __init__(self):
        genericgame.Game.__init__(self)
        self.num_player=(2,8)
        self.players=0
        self.name="Culo"
        self.caption="Titulo de la Ventana (Culo)"
        self.num=0
        self.c=core.Core()

        self.caption="Culo"
        self.ai=AI()
        self.game=self.c.get_app()['gamezone']
        #self.deckdraws=[{"name":"Mazo para robar","numbers":["As",2,3,4,5,6,7,"J","Q","K"],"suits":["espadas","oros","bastos","copas"]}]
        #self.playzone=True
        
        #self.throws=[]

        actions=type('actions', (), {
		'select':lambda *a,**k:None,
		'clear_selection':lambda *a,**k:None,
		'throw_cards':lambda *a,**k:None,
		'end_turn':lambda *a,**k:None,
		'sort_by_points':lambda *a,**k:None,
		'draw_a_card':lambda *a,**k:None,
		'pass_turn':lambda *a,**k:None,})
		
        self.down_func={
            pygame.K_DOWN   :   [pygame.display.toggle_fullscreen,[]] , \
            pygame.K_ESCAPE :   sys.exit, \
            pygame.K_F5     :   self.game.show, \
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

    def init_game(self):
        pass

    def init_round(self):
        """
        crea mazos, y reparte las cartas entre los jugadores
        """
        pass

    def is_round_finished(self):
        pass
        
    def end_of_round(self):
        pass
    
    def init_turn(self):
        pass

    def terminable_turn(self):
        pass
        
    def pass_turn(self):
        pass
    
    def end_turn(self):
        pass
    
    def ending_turn():
        pass
        
    def throw_cards(self):
        pass
        
    def throwable_selection(self,selection):
        pass
        
    def select(self):
        """
        esta funcion se llamará tras producirse la seleccion.
        consejos de uso: en un juego donde solo se pueda tirar una carta
        al seleccionarse con esta funcion se puede hacer que se mande
        automaticamente
        """
        pass
        
    def clear_selection(self):
        """
        se llama tras limpiar la seleccion, por si el juego tuviera
        algun contador de cartas seleccionadas o algun otro tipo de registro
        """
        pass
        
    def draw_a_card(self):
        """
        roba una carta del mazo correspondiente
        """
        pass
        
    def deal(self):
        pass
        
    def data_for_results(self, rounds):
        pass
        
    def get_points(self, selection):
        pass
