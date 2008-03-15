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
        except: pass
        self.gz.show()
        
    def clear_selection(self,player=-1):
        self.player=player
        self.player.clear_selection_from_deck()
        try: self.rules.clear_selection()
        except: pass
        self.gz.show()
    
    #entre mazos    
    def throw_cards(self,player=-1):
        self.player=player
        selection=self.player.get_selection_from_deck()                
        if self.throwable_selection(selection):#and self.gz.p[self.gz.pwt].clickable:
            self.player.send(self.gz.playzone[self.gz.playzone_active])
            self.gz.throws.append(selection)
            try: self.rules.throw_cards(selection)
            except: pass
            self.gz.show()
            
            
            
            
    
    def throwable_selection(self,selection):
        try: r=self.rules.throwable_selection(selection)
        except: r=True
        finally: return r
    
    def draw_a_card(self,n=1,player=-1):
        self.player=player
        self.player.draw_a_card(self.gz.deckdraws[0],n)
        try: self.rules.draw_a_card()
        except: pass
        self.gz.draw.show()
        
    def deal(self,n):
        self.gz.deckdraws[0].deal(n,self.gz.p)
        try: self.rules.deal()
        except: pass
        self.gz.show()
    
    #otras
    def pass_turn(self):
        self.gz.pass_turns_counter+=1
        self.rules.pass_turn()
        try: self.rules.pass_turn()
        except: pass
        self.ending_turn(pass_turn=True)
        
    def end_turn(self):
        if self.gz.terminable_turn:
            try: self.rules.end_turn()
            except: pass
            self.ending_turn()
            
    def ending_turn(self,pass_turn=False):
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
        except: pass
        self.gz.show()
        try: self.rules.new_turn()
        except: pass
    
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
        
    def exit(self):
        gamezone.exit()
    
    def show(self):
        gamezone.show()
        
    def __getattr__(self, attr):
        if attr=="player":
            return self.gz.p[self.p]
            
    def __setattr__(self, attr, value):
        if attr=="player" and value ==-1:
            try: self.__dict__["p"] = self.gz.player_with_turn
            except:pass
        elif attr=="player":
            self.__dict__["p"] = value
        else:
            self.__dict__[attr] = value
