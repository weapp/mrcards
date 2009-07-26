import random

class Deck(object):
    def __init__(self, cards=[], visible=[], maxcards=-1):
        self.visible = visible[:]
        self.max = maxcards
        self.cards = []
        self.add_cards(cards)
    
    @property
    def selection(self):
        return [card for card in self if card.selected]  #filtra las cartas seleccionadas
    
	"""
    @selection.setter
    def selection(self, n):
        if  n <len(self.cards):
            self.cards[n].select()
    """
    @selection.setter
    def selection(self, cards): #no funciona :S
        for card in cards:
            self.select(card)
    	
    @selection.deleter
    def selection(self):
		for card in self:
			card.selected = False
    
    def select(self, card):
        if card in self:
            card.select()
	
	
    #reordenar mazos
    def shuffle(self):
        random.shuffle(self)    
        
    def sort_by_suit(self): #palo
        self.sort(CmpAttr("suit"))
        
    def sort_by_number(self):
        self.sort(CmpAttr("number"))
        
    #cambiar cartas entre mazos
    def deal(self, n, decks):#repartir
        for i in range(n):
            for deck in decks:
                deck.draw_a_card(self, 1)
    
    def draw_a_card(self, deck, n=1):
        #for i in range(len(self)):
        for i in range(n):
            if len(deck) > 0:
                if self.add_card(deck[0]):
                    deck.rem_card(deck[0])
        #pass#robar,si no se le indica nada se utilizara el mazo definido arriba.
    
    def send(self,deck):#la seleccion #eviar a un jugador o zona
        #TODO se deberia comprobar si el mazo admite cartas
        selection=self.selection
        del self.selection
        deck.add_cards(selection)
        self.rem_cards(selection)
        
    
    def add_card(self,card):
        if self.max==-1 or self.max>len(self):
            card.change_owner(self)
            self.cards.append(card)
            card.setVisibility(self.visible)
            return True
        else: return False
        
    def add_cards(self, cards):
        counter_cards=0
        for card in cards:
            if self.add_card(card):
                counter_cards += 1
        return counter_cards
    
    def rem_card(self,card):
        if card in self.cards:
            self.cards.remove(card)
            
    def rem_cards(self,cards):
        for card in cards:
            self.rem_card(card)
    
    def count_points(self):
        points = 0
        for card in self:
            point += card.get_points()
        return points
                

    
    #sfunciones magicas        
    def __str__(self):
		r = "<< "
		for i in range(len(self)):
			if not i == 0:
				r += ", "
			r += str(self[i])
		r += " >>"
		return r
    __repr__=__str__ 
	
    def __id__(self):
        r = ""
        for card in self:
            r += str(card)
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
        
    def clear(self):
        del self.cards[:]
        
    def sort(self, comparator):
        self.cards.sort(comparator)
    
class CmpAttr:
    def __init__(self, attr):
        self.attr = attr
    def __call__(self, x, y):
        return cmp(getattr(x, self.attr), getattr(y, self.attr))
