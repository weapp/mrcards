import deck
import draw
import sys
import pygame
import os


class gamezone:

    def set_down_func(self,down_func):
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit

    def set_up_func(self,up_func):
        self.up_func=up_func

    def __init__(self,game_rules=False,caption="Untitled",down_func={},up_func={}):
        self.rules=game_rules
        self.keys_decriptions="F5:Reload  Esc:Exit  Down:Toggle Fullscreen  D:Draw a card\n" + \
                              "[1-10]:Add to/Rem from Selection  Z:Clear Selection  T,Return:Throws \n" + \
                              "E:End Turn  S:Sort by suit N:Sort by number  P:sort by points"
        self.terminable_turn=True

        self.draw=draw.draw(self,caption)
        
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit
        
            
        self.up_func=up_func
        self.player_with_turn=0
        self.clockwise_direction=True
        self.pass_turns_counter=0 #contador de turnos sin tiradas
        self.round=0
        self.turn=0
        self.players=[]
        self.deckdraws=[]
        self.deckdiscard=[]
        self.deckpoints=[]
        self.playzone=[]
        self.selection=deck.deck(id_deck="selection",visible=True)
        self.player_default=0
        self.playzone_default=0
        self.playzone_active=self.playzone_default
        self.deckdiscard_active=0
        
        
        try: self.keys_descriptions=rules.keys_descriptions
        except: pass
        try: self.terminable_turn=rules.terminable_turn
        except: pass
        
        
        
        try: self.player=self.players[self.player_with_turn]
        except: pass
        
    #seleccionar
    def select(self,n):
        if n<len(self.player.cards):#self.player.clickable and 
            self.player.cards[n].select_card()
            try: self.rules.select()
            except: pass
            self.show()
        
    def clear_selection(self):
        #if self.player.clickable:
        self.player.clear_selection_from_deck()
        try: self.rules.clear_selection()
        except: pass
        self.show()
    
    #entre mazos    
    def throw_cards(self,playzone=None):
        selection=self.player.get_selection_from_deck()
        if self.throwable_selection(selection):
            #if self.player.clickable:
            if playzone==None:
                playzone=self.playzone[self.playzone_active]
            self.player.send(playzone)
            try: self.rules.throw_cards(selection)
            except: pass
            self.show()
    
    def throwable_selection(self,selection):
        try: r=self.rules.throwable_selection(selection)
        except: 
            r=True
        finally:
            return r
    
    def draw_a_card(self,n=1):
        self.player.draw_a_card(self.deckdraws[0],n)
        try: self.rules.draw_a_card()
        except: pass
        self.draw.show()
        
    def deal(self,n):
        self.deckdraws[0].deal(n,self.players)
        try: self.rules.deal()
        except: pass
        self.draw.show()
    
    #anyadir
    def add_playzone(self,id_deck,cards=[[],[]],visible=False,maxcards=0,clickable=False,point=False):
        if point:
            playzone=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            playzone=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.playzone.append(playzone)
        #self.playzone.append(playzone)
    
    def add_deckdraw(self,id_deck,cards=[[],[]],visible=False,maxcards=0,clickable=False,point=False):
        if point:
            deckdraw=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            deckdraw=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.deckdraws.append(deckdraw)
    
    
    def add_deckdiscard(self,deckdiscard):
        self.deckdiscard.append(deckdiscard)
    
    def add_deckpoints(self,deckpoints):
        self.deckpoints.append(deckpoints)
    
    def add_player(self,id_deck,cards=[[],[]],visible = None,maxcards=0,clickable=None,point=False):
        if visible == None:
            if len(self.players)==self.player_default:
                visible=True
            else:
                visible=False
                
        if clickable == None:
            if len(self.players)==self.player_default:
                clickable=True
            else:
                clickable=False
        
        if point:
            player=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            player=deck.deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)
        self.players.append(player)
        self.player=self.players[self.player_with_turn]
    
    def show(self):
        self.draw.show()
        print self
    
    
        #acciones especiales
    def pass_turn(self):
        self.pass_turns_counter+=1
        try: self.rules.pass_turn()
        except: pass
        self.ending_turn(pass_turn=True)
        
    def end_turn(self):
        if self.terminable_turn:
            try: self.rules.end_turn()
            except: pass
            self.ending_turn()
            
    def ending_turn(self,pass_turn=False):
        if not pass_turn:
            self.pass_turns_counter=0
        if self.clockwise_direction:
            self.player_with_turn+=1
        else:
            self.player_with_turn-=1
        if self.player_with_turn==0:
            self.turn+=1
        self.player_with_turn%=len(self.players)
        self.player=self.players[self.player_with_turn]
        try: self.rules.ending_turn()
        except: pass
        self.show()

        
        
    def stick(self):
        pass#plantarse o retirarse TODO no puede estar bien, no es lo mismo no apostar mas que dejar el juego
        
        #acciones
    def discard(self,deckdiscard=None):
        #if self.player.clickable:
        if deckdiscard==None:
            deckdiscard=self.deckdiscard[self.deckdiscard_active]
        self.player.send(deckdiscard)
        self.show()
        
    def sort_by_suit(self):
        player=self.players[self.player_with_turn]
        player.sort_by_suit()
        self.show()
        
    def sort_by_number(self):
        self.player.sort_by_number()
        self.show()
        
    def sort_by_points(self):
        self.player.sort_by_points()
        self.show()
    
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
        for card in self.players[0].get_selection_from_deck():
            r+=" "+str(card)+""
        r+="\n\nSelection (jug actual):"
        r+="\n    "
        for card in self.player.get_selection_from_deck():
            r+=" "+str(card)+""
        r+="\n\n______________________"
        r+="\n"+self.keys_decriptions
        #self.show()
        return r
    
    
    
    def init_bucle(self):
        self.clock = pygame.time.Clock()
        # Bucle principal
        while True:
            self.clock.tick(40)
                
            # control de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                #actualiza el screen para que cuando se cambie a pantalla completa se vea con la nueva resolucion
                if event.type == pygame.VIDEORESIZE: 
                    self.screen = pygame.display.set_mode(event.size, pygame.DOUBLEBUF | pygame.HWSURFACE |  pygame.RESIZABLE ) 
                    ##print self.screen
                    self.show()
                    

                # si no es un evento de teclado o raton, lo ignoramos
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
                    if (dic_func.has_key(event.key)):
                        
                        if(type(dic_func[event.key])==type([])):
                            tmp_fun=dic_func[event.key][0]
                            tmp_arg=dic_func[event.key][1]
                            
                            if(type(tmp_arg)==type({})):
                                tmp_fun( **tmp_arg )
                            elif(type(tmp_arg)==type([]) or type(tmp_arg)==type(())):
                                tmp_fun( *tmp_arg )
                            else:
                                tmp_fun(tmp_arg)
                        else:
                            dic_func[event.key]()

            # Refresco de pantalla
            pygame.display.flip()    




def pint(self,x="tecla",y="pulsada"):
    print "evento:",x,y
