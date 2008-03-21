#self.gz.p[self.gz.pwt]

class Actions:
    def __init__(self,gamezone,rules):
        self.gz=gamezone
        rules=__import__("rules/"+rules)
        self.rules=rules.Game(self.gz,self)
        
    #seleccionar
    def select(self,n,player=-1):
        self.player=player
        self.player.select(n)
        try: self.rules.select()
        except AttributeError: pass
        self.gz.show()
        
    def clear_selection(self,player=-1):
        self.player=player
        self.player.clear_selection_from_deck()
        try: self.rules.clear_selection()
        except AttributeError: pass
        self.gz.show()
    
    #entre mazos    
    def throw_cards(self,player=-1):
        self.player=player
        selection=self.player.get_selection_from_deck()                
        if self.throwable_selection(selection):#and self.gz.p[self.gz.pwt].clickable:
            self.player.send(self.gz.playzone[self.gz.playzone_active])
            self.gz.throws.append(selection)
            try: self.rules.throw_cards(selection)
            except AttributeError: pass
            self.gz.show()
            
            
            
            
    
    def throwable_selection(self,selection):
        try: r=self.rules.throwable_selection(selection)
        except AttributeError: r=True
        return r
    
    def draw_a_card(self,n=1,player=-1):
        self.player=player
        self.player.draw_a_card(self.gz.deckdraws[0],n)
        try: self.rules.draw_a_card()
        except AttributeError: pass
        self.gz.draw.show()
        
    def deal(self,n):
        self.gz.deckdraws[0].deal(n,self.gz.p)
        try: self.rules.deal()
        except AttributeError: pass
        self.gz.show()
    
    #otras
    def pass_turn(self,player=-1):
        self.player=player
        self.gz.pass_turns_counter+=1
        try: self.rules.pass_turn()
        except AttributeError: pass
        self.ending_turn(pass_turn=True)
        
    def end_turn(self,player=-1):
        self.player=player
        if self.gz.terminable_turn:
            try: self.rules.end_turn()
            except AttributeError: pass
            self.ending_turn()
            
    def ending_turn(self,pass_turn=False):
        self.clear_selection()
        if not pass_turn:
            self.gz.pass_turns_counter=0
        if self.gz.clockwise_direction:
            self.gz.player_with_turn+=1
        else:
            self.gz.player_with_turn-=1
        if self.gz.pwt==0:
            self.gz.turn+=1
        self.gz.player_with_turn%=len(self.gz.p)
        self.gz.player=self.gz.p[self.gz.pwt]
        try: self.rules.ending_turn()
        except AttributeError: pass
        self.gz.show()
        try: self.rules.new_turn()
        except AttributeError: pass
    
    def clear_playzone(self):
        del self.gz.playzone[0].cards[:]
        
    def stick(self):
        pass#plantarse o retirarse TODO no puede estar bien, no es lo mismo no apostar mas que dejar el juego
        
    def discard(self,deckdiscard=None,player=-1):
        self.player=player
        #if self.gz.p[self.gz.pwt].clickable:
        if deckdiscard==None:
            deckdiscard=self.gz.deckdiscard[self.gz.deckdiscard_active]
        self.player.send(deckdiscard)
        self.gz.show()
        
    #ordenar
    def sort_by_suit(self,player=-1):
        self.player=player
        self.player.sort_by_suit()
        self.gz.show()
        
    def sort_by_number(self,player=-1):
        self.player=player
        self.player.sort_by_number()
        self.gz.show()
        
    def sort_by_points(self,player=-1):
        self.player=player
        self.player.sort_by_points()
        self.gz.show()
        
    def sort(self,by):
        if by=="suit":
            self.gz.globaleventlist.append([self.gz.user,"self.actions.sort_by_suit()"])
        elif by=="number":
            self.gz.globaleventlist.append([self.gz.user,"self.actions.sort_by_number()"])
        elif by=="points":
            self.gz.globaleventlist.append([self.gz.user,"self.actions.sort_by_points()"])
        
    def exit(self):
        self.gz.exit()
    
    def showalt(self):
        if self.gz.show_layer_alternative:
            self.gz.show_layer_alternative = False
        else:
            self.gz.show_layer_alternative = True
        self.show()
    
    def show(self):
        self.gz.show()
        
    def F(self,f=0):
        for player in self.gz.players:
            for card in player.cards:
                card.setVisibility(False)
                
        if f!=10 and f<len(self.gz.players):
            self.gz.user=f
            self.gz.players[f].visible=False
            
            for card in self.gz.players[f].cards:
                card.setVisibility(True)
        self.show()
        
    def F1(self):
        self.F(0)
    def F2(self):
        self.F(1)
    def F3(self):
        self.F(2)
    def F4(self):
        self.F(3)
    def F12(self):
        self.F(10)
        
    
    def __getattr__(self, attr):
        if attr=="player":
            return self.gz.p[self.p]
            
    def __setattr__(self, attr, value):
        if attr=="player" and value ==-1:
            try: self.__dict__["p"] = self.gz.player_with_turn
            except AttributeError:pass
        elif attr=="player":
            self.__dict__["p"] = value
        else:
            self.__dict__[attr] = value
