import pygame
import sys
import card
from math import sin, cos,pi
import random

def point1(num,suit):
    return 1

class Deck:
    def __init__(self,id_deck,cards=[[],[]],visible=False,maxcards=10,clickable=False,point=point1):
        self.id=id_deck
        self.visible=visible
        self.max=maxcards
        self.clickable=clickable
        self.cards = []
        self.point = point
        
        for num in cards[0]:
            for suit in cards[1]:
                self.cards.append(card.Card(card_id=str(num)+str(suit),owner=self.id,number=num,suit=suit,visible=visible,points=point(num,suit)))    
                
    def getx(self):
        selected=[]
        for card in self.cards:
            if card.is_selected():
                selected.append(card)
        return selected

    def setx(self, x):
        pass

    selection = property(getx, setx)
        

    
    #maximo
    def get_max(self):
        return self.max
    
    def set_max(self,n):
        self.max=n
    
    #reordenar mazos
    def shuffle(self):
        random.shuffle(self)    
        
    def sort_by_suit(self):#palo
        self.sort(CmpAttr("suit"))
        
    def sort_by_number(self):
        self.sort(CmpAttr("number"))
        
    def sort_by_points(self):
        self.sort(CmpAttr("points"))
    
    #cambiar cartas entre mazos
    def deal(self,n,decks):#repartir
        for i in range(n):
            for deck in decks:
                deck.draw_a_card(self,1)
    
    def draw_a_card(self,deck,n=1):
        #for i in range(len(self)):
        for i in range(n):
            if len(deck)>0:
                self.add_card(deck[0])
                deck.rem_card(deck[0])
        #pass#robar,si no se le indica nada se utilizara el mazo definido arriba.
    
    def send(self,deck):#la seleccion #eviar a un jugador o zona
        selection=self.selection
        deck.add_cards(selection)
        self.clear_selection_from_deck()
        self.rem_cards(selection)
    
    def add_card(self,card):
        card.change_owner(self)
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
            point+=card.get_points()
        return points
                
    #seleccion de cartas
    def select(self,n):
        if n<len(self.cards):#self.clickable and 
            self.cards[n].select_card()
            
    def select_card(self,card):
        for icard in self:
            if id(card) == id(icard):
                card.select_card()
            
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
        
    def __id__(self):
        r=""
        for card in self:
            r+=str(card)
        return self.id + ": " + r
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, clave):
        return self.cards[clave]
        
    def __setitem__(self, clave, valor):
        self.cards[clave]=valor
    
    def __delitem__(self, clave):
        del self.cards[clave]
        
    def __getslice__(self, i, j):
        return self.cards[i:j]
        
    def __setslice__(self, i, j, secuencia):
        self.cards[i:j]=secuencia
        
    def __delslice__(self, i, j):
        del self.cards[i:j]
        
    def __iter__(self):
        return iter(self.cards)
        

        
    def sort(self,comparator):
        self.cards.sort(comparator)
    
class CmpAttr:
    def __init__(self, attr):
        self.attr = attr
    def __call__(self, x, y):
        return cmp(getattr(x, self.attr), getattr(y, self.attr))
