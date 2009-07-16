#!/usr/bin/env python
#-*- coding:utf-8 -*-
from library.general import singleton

class Game:
    __metaclass__ = singleton.Singleton
    def __init__(self):
        self.num_player=(0,0)
        self.players=0
        self.name=""
        self.caption=self.name
        self.playzone=False
        self.deckdraws=[]
        self.down_func={}

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
        
    def update(self):
        pass
