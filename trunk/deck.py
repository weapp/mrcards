import pygame
import sys
import card
from math import sin, cos,pi
import random

def point1(num,suit):
    return 1

class deck:
    def __init__(self,id_deck,cards=[[],[]],visible=False,maxcards=10,clickable=False,point=point1):
        self.id=id_deck
        self.visible=visible
        self.max=maxcards
        self.clickable=clickable
        self.cards = []
        self.point = point
        
        for num in cards[0]:
            for suit in cards[1]:
                self.cards.append(card.card(card_id=str(num)+str(suit),owner=self.id,number=num,suit=suit,visible=visible,points=point(num,suit)))    
    
    #maximo
    def get_max(self):
        return self.max
    
    def set_max(self,n):
        self.max=n
        
    #reordenar mazos
    def shuffle(self):
        random.shuffle(self.cards)    
        
    def sort_by_suit(self):#palo
        self.cards.sort(CmpAttr("suit"))
        
    def sort_by_number(self):
        self.cards.sort(CmpAttr("number"))
        
    def sort_by_points(self):
        self.cards.sort(CmpAttr("points"))

    #cambiar cartas entre mazos
    def deal(self,n,decks):#repartir
        for i in range(n):
            for deck in decks:
                deck.draw_a_card(self,1)
    
    def draw_a_card(self,deck,n=1):
        #for i in range(len(self.cards)):
        for i in range(n):
            if len(deck.cards)>0:
                self.add_card(deck.cards[0])
                deck.rem_card(deck.cards[0])
        #pass#robar,si no se le indica nada se utilizara el mazo definido arriba.
    
    def send(self,deck):#la seleccion #eviar a un jugador o zona
        selection=self.get_selection_from_deck()
        deck.add_cards(selection)
        self.clear_selection_from_deck()
        self.rem_cards(selection)
    
    def add_card(self,card):
        self.cards.append(card)
        card.setVisibility(self.visible)
        
    def add_cards(self,cards):
        for card in cards:
            self.add_card(card)
    
    def rem_card(self,card):
        if card in self.cards:
            self.cards.remove(card)
            
    def rem_cards(self,cards):
        for card in cards:
            self.rem_card(card)
    
    def count_points(self):
        points=0
        for card in self.cards:
            point+=card.getPoints()
        return points
                
    #seleccion de cartas                               ----- TERMINADO
    def clear_selection_from_deck(self):
        for card in self.cards:
            card.remove_from_selection()
            
    def get_selection_from_deck(self):        
        selected=[]
        for card in self.cards:
            if card.is_selected():
                selected.append(card)
        return selected
    
    ##funciones magicas        
    def __str__(self):
        if self.visible:
            r="< "
            for i in range(len(self.cards)):
                if not i == 0:
                    r+=", "
                r+=str(self.cards[i])
            r+=" >"
        else:
            r="#"
        return self.id + ": " + r
            
class CmpAttr:
    def __init__(self, attr):
        self.attr = attr
    def __call__(self, x, y):
        return cmp(getattr(x, self.attr), getattr(y, self.attr))
