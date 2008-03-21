import deck
import drawer
import sys
import pygame
import os
import actions

class Gamezone:
    def __init__(self,rules=False,down_func={},up_func={}):
        self._counter=0        
        
        self.actions=actions.Actions(self,rules)
        self.rules=self.actions.rules
        self.drawer=drawer.Drawer(self,caption=self.rules.caption)
        self.keys_descriptions="Esc:Exit"
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit
        
        self.up_func=up_func
        self.player_with_turn=0
        self.clockwise_direction=True
        self.pass_turns_counter=0 # contador de turnos sin tiradas
        self.round=0
        self.turn=0
        self.players=[]
        self.deckdraws=[]
        self.deckdiscard=[]
        self.deckpoints=[]
        self.playzone=[]
        
        self.selection=deck.Deck(self.counter,id_deck="selection",visible=True)
        self.throws=[]
        
        self.player_default=0
        self.playzone_default=0
        self.playzone_active=self.playzone_default
        self.deckdiscard_active=0
        self.user = self.player_default
        
        self.localeventlist=[]
        self.globaleventlist=[]
        
        try: self.keys_descriptions=self.rules.keys_descriptions
        except AttributeError: pass
    
    def get_counter(self):
        ++self._counter
        return self._counter
        
    def __getattr__(self,attr):
        if attr=="counter":
            ++self._counter
            return self._counter
        if attr=="p":
            return self.players
        elif attr=="pwt":
            return self.player_with_turn
        elif attr=="last_throw":
            return self.throws[len(self.throws)-1]
        elif attr=="terminable_turn":
            try: return rules.terminable_turn()
            except AttributeError: return True
        elif attr=="player":
            try: return self.players[self.player_with_turn]
            except: pass
        else:
            print "\n    INTENTANDO ACCEDER A ATRIBUTO NO EXISTENTE:", attr,"\n"
            raise AttributeError("Gamezone instance has no attribute '"+str(attr)+"'")
            
    def __setattr__(self, attr, value):
        if attr=="p":
            self.players=value
        elif attr=="pwt":
            self.player_with_turn=value
        elif attr=="player":
            try: self.players[self.player_with_turn]=value
            except AttributeError: pass
        else:
            self.__dict__[attr] = value

        
    def set_down_func(self,down_func):
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit

    def set_up_func(self,up_func):
        self.up_func=up_func

    # Anyadir mazos
    def add_playzone(self,id_deck,cards=[[],[]],visible=False,maxcards=0,clickable=False,point=False):
        if point:
            playzone=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            playzone=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.playzone.append(playzone)
    
    def add_deckdraw(self,id_deck,cards=[[],[]],visible=False,maxcards=0,clickable=False,point=False):
        if point:
            deckdraw=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            deckdraw=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.deckdraws.append(deckdraw)
    
    
    def add_deckdiscard(self,deckdiscard):
        self.deckdiscard.append(deckdiscard)
    
    def add_deckpoints(self,deckpoints):
        self.deckpoints.append(deckpoints)
    
    def add_player(self,id_deck,cards=[[],[]],visible = None,maxcards=0,clickable=None,point=False):
        if visible == None:
            if len(self.players)==self.user:
                visible=True
            else:
                visible=False
                
        if clickable == None:
            if len(self.players)==self.user:
                clickable=True
            else:
                clickable=False
        
        if point:
            player=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            player=deck.Deck(self.counter,id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.players.append(player)
        self.player=self.players[self.player_with_turn]



    
    def __str__(self):
        r="_________GAME_________"
        r+="\n\nDraw Decks:"
        for deck in self.deckdraws:
            r+="\n    "+str(deck)
            
        r+="\n\nPlayer Decks:"
        for deck in self.players:
            r+="\n    "+str(deck)
        r+="\n\nPlay Zone:"
        for deck in self.playzone:
            r+="\n    "+str(deck)
        r+="\n\nSelection:"
        r+="\n    "
        for card in self.players[self.user].selection:
            r+=" "+str(card)+""
        r+="\n\nSelection (jug actual):"
        r+="\n    "
        for card in self.players[self.player_with_turn].get_selection_from_deck():
            r+=" "+str(card)+""
        r+="\n\n______________________"
        r+="\n"+self.keys_descriptions
        #self.show()
        return r

    # Pintar
    def show(self):
        self.drawer.show()
        print self


    # Bucle principal
    def init_bucle(self):
        self.clock = pygame.time.Clock()
        
        while True:
            self.clock.tick(40)
                
            # Control de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                # Actualiza el screen para que cuando se cambie a pantalla completa se vea con la nueva resolucion
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(event.size, pygame.DOUBLEBUF | pygame.HWSURFACE |  pygame.RESIZABLE ) 
                    #print self.screen
                    self.show()
                    

                # Si no es un evento de teclado o raton, lo ignoramos
                if not hasattr(event,'button') and not hasattr(event,'key'):
                    continue
                
                # Eventos de raton
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print "boton" + str(event.button)
                
                
                # Eventos de teclado
                if event.type == pygame.KEYDOWN:
                    dic_func=self.down_func
                elif event.type == pygame.KEYUP:
                    dic_func=self.up_func
                            
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if dic_func.has_key(event.key):# and self.player_with_turn == self.user:
                        
                        if type(dic_func[event.key])==type([]):
                            tmp_fun=dic_func[event.key][0]
                            tmp_sco=dic_func[event.key][1] #scope:ambito:local,global
                            
                            if tmp_sco=="global":
                                if self.user==self.pwt:
                                    self.globaleventlist.append([self.user,tmp_fun])
                            else:
                                print eval(tmp_fun)

                            print self.globaleventlist
                            
                            for event in self.globaleventlist:
                                if event[1][-2:-1]=="(":
                                    eval (str(event[1][:-1])+"player="+str(event[0])+")")
                                else:
                                    eval (str(event[1][:-1])+",player="+str(event[0])+")")
                                del self.globaleventlist[self.globaleventlist.index(event)]
                        else:
                            dic_func[event.key]()
 

            # Refresco de pantalla
            pygame.display.flip()

    def exit(self):
        sys.exit()
        
    def __iter__(self):
        return iter([self.players, self.deckdraws, self.deckdiscard, self.deckpoints, self.playzone])
