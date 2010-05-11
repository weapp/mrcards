import pygame
import sys
class Card:
    def __init__(self, card_id, owner, number=False, suit="special", visible=False, points=1):
        self.id=card_id
        self.suit=suit
        self.number=number
        self.points=points
        self.visible=visible
        self.selected = False # ? pasa a convertirse en un nuevo mazo ?
        self.actual_owner=owner#propietario
        self.previous_owner=False
        
        
    def getNum(self):
        return self.number
                
    def flipcard(self):
        if self.visible:
            self.visible=False
        else:
            self.visible=True
            
    def setVisibility(self, new_visibility):
        self.visible=new_visibility
    
    def get_Id(self):
        return self.id
    
    def get_suit(self):
        return self.suit
    
    def get_number(self):
        return self.number
        
    def get_points(self):
        return self.points
    
    def is_visible(self):
        return self.visible
        
        
    def change_owner(self, new_owner):
        self.previous_owner=self.actual_owner
        self.actual_owner=new_owner

#seleccion de cartas                               ----- TERMINADO
    def select_card(self):#si no esta seleccionada: seleccionar. si lo esta: eliminar
        if self.is_selected():
            self.remove_from_selection()
        else:
            self.add_to_selection()

    def is_selected(self):
        return self.selected
        
    def add_to_selection(self):
        self.selected=True
      
    def remove_from_selection(self):
        self.selected=False
    

    
    def __str__(self):
        if self.visible:
            #return "["+str(self.id) + ":" + str(self.number) + " de " + str(self.suit) + "("+str(self.points)+"p)]"
            return "[" + str(_(self.number)) + " " + str(_(self.suit)) + "]"
        else:
            return "#"

    
    def __id__(self):
        return "[" + str(self.number) + " " + str(self.suit) + "]"
        
    def __cmp__(self, other):
            return cmp(self.id, other.id)
        
    def cmpSuit(self, other):
        return cmp(self.getSuit(), other.getSuit())
        
    def cmpNum(self, other):
        return cmp(self.getNum(), other.getNum())