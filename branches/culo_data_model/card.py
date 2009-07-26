import pygame
import sys
class Card(object):
    def __init__(self, number=0, suit="special", visible=[]):
        #self.id=card_id
        self.suit=suit
        self.number=number
        self.visible=visible
        self.selected = False # ? pasa a convertirse en un nuevo mazo ?
        self.actual_owner=None
        self.previous_owner=None
        
    def getNum(self):
        return self.number
    
	"""
    def flipcard(self):
        if self.visible:
            self.visible=False
        else:
            self.visible=True
    """
	
    def setVisibility(self, new_visibility):
        self.visible=new_visibility
    
    def get_Id(self):
        return self.id
    
    def get_suit(self):
        return self.suit
    
    def get_number(self):
        return self.number
        
        
    def change_owner(self, new_owner):
        self.previous_owner=self.actual_owner
        self.actual_owner=new_owner

#seleccion de cartas                               ----- TERMINADO
    def select(self):#si no esta seleccionada: seleccionar. si lo esta: eliminar
        self.selected = not self.selected
    
    def __str__(self):
        t="#" if self.selected else " "
        return "[%s%s%s]" % (t , str(self.number), str(self.suit))
    
    def __id__(self):
        return "[" + str(self.number) + " " + str(self.suit) + "]"
    """
    def __cmp__(self, other):
            return cmp(self.id, other.id)
    """ 
    def cmpSuit(self, other):
        return cmp(self.getSuit(), other.getSuit())
        
    def cmpNum(self, other):
        return cmp(self.getNum(), other.getNum())
