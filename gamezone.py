import os
import sys
import pygame
import socket
from deck import Deck
from drawer import Drawer
from library import core
from pars import name_players

class Gamezone:
    def __init__(self,rules=False,down_func={},up_func={}, netobj=None):
        self.core=core.Core()
        self.show_layer_alternative=False
        self.rules=rules
        self.drawer=Drawer(self,caption=self.rules.caption)
        self.keys_descriptions="Esc:Exit"
        self.down_func=down_func
        self.down_func.setdefault(pygame.K_ESCAPE,sys.exit)
        self.up_func=up_func
        self.player_with_turn=0
        self.clockwise_direction=True
        self.pass_turns_counter=0 # contador de turnos sin tiradas
        self.round=0
        self.turn=0 #TODO: vueltas k lleva la partida
        self.deckdraws=[]
        self.deckdiscard=[]
        self.deckpoints=[]
        self.playzone=[]
        
        self.throws=[]
        
        self.player_default=0 # jugador que toma el usuario por defecto (server o el k no es IA)
        self.playzone_default=0
        self.playzone_active=self.playzone_default
        self.deckdiscard_active=0 # TODO
        self.user = self.player_default
        
        self.localeventlist=[] # no se utiliza
        self.globaleventlist=[]

        self.net = netobj

        if hasattr(self.rules,'keys_descriptions'):self.keys_descriptions=self.rules.keys_descriptions
        
        self._counter=0
        self.player_with_turn=0
        self.pass_turns_counter=0

    
    def get_player(self):
        return self.app['players'][self.player_with_turn]
    
    def get_terminable_turn(self):
        return self.rules.terminable_turn()
        
    def get_last_throw(self):
        return self.throws[len(self.throws)-1]
        
    def set_player(self,new_value):
        self.app['players'][self.player_with_turn]=new_value
        
    def set_down_func(self,down_func):
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit

    def set_up_func(self,up_func):
        self.up_func=up_func

    # Anyadir mazos
    def add_playzone(self, id_deck, cards=[[], []], visible=False, maxcards=0, clickable=False, point=False):
        if point:
            playzone = Deck(id_deck=id_deck, cards=cards, visible=visible, maxcards=maxcards, clickable=clickable, point=point)
        else:
            playzone = Deck(id_deck=id_deck, cards=cards, visible=visible, maxcards=maxcards, clickable=clickable)
        self.playzone.append(playzone)
    
    def add_deckdraw(self, deckdraw):
        self.deckdraws.append(deckdraw)
    
    def add_deckdiscard(self, deckdiscard):
        self.deckdiscard.append(deckdiscard)
    
    def add_deckpoints(self, deckpoints):
        self.deckpoints.append(deckpoints)
    
    def add_player(self, id_deck, cards=[[], []], visible = None, maxcards=0, clickable=None, point=False):
        if visible == None:
            if len(self.app['players'])==self.user:
                visible=True
            else:
                visible=False
        if clickable == None:
            if len(self.app['players']) == self.user:
                clickable = True
            else:
                clickable = False
        if point:
            player=Deck(id_deck=id_deck, cards=cards, visible=visible, \
                        maxcards=maxcards, clickable=clickable, point=point)
        else:
            player=Deck(id_deck=id_deck, cards=cards, visible=visible, \
                        maxcards=maxcards, clickable=clickable)
        self.app['players'].append(player)
        self.player = self.app['players'][self.player_with_turn]

    def __repr__(self):
        return 'repr DE GAMEZONE'
        
    def __str__(self):
        players = self.app.m['players']
        r="_________GAME_________"
        r+="\n\n"+("Draw Decks")+":"
        for deck in self.app.m['deckdraws']:
            r+="\n    "+str(deck)
            
        r+="\n\n"+("Player Decks")+":"
        for deck in players:
            r+="\n    "+str(deck)
            
        r+="\n\n"+("Play Zone")+":"
        for deck in players:
            r+="\n    "+str(deck)
        r+="\n\n"+("Selection")+":"
        r+="\n    "
		
        for card in players[name_players[self.user]].selection:
            r+=" "+str(card)+""
        r+="\n\n"+("Selection")+" ("+("player with turn")+"):"
        r+="\n    "
        for card in players[name_players[self.player_with_turn]].get_selection_from_deck():
            r+=" "+str(card)+""
        r+="\n\n______________________"
        r+="\n"+self.keys_descriptions
        #self.show()
        return r

    # Pintar
    def show(self):
        self.drawer.show()
        print self
    
    
    def __iter__(self):
        return self.app.values()


    def new_event(self,event):
        # Actualiza el screen para que cuando se cambie a pantalla
        # completa se vea con la nueva resolucion
        if event.type == pygame.VIDEORESIZE:
            self.core.set_size(event.size)
            self.screen = self.core.get_screen() 
            #self.screen = pygame.display.get_surface()
            #self.screen.set_clip(0,0,*event.size)
            #print self.screen
            self.show()
        
        # Si no es un evento de teclado o raton, lo ignoramos
        if hasattr(event,'button') and hasattr(event,'key'):
            # Eventos de raton
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "boton" + str(event.button) + str(pygame.mouse.get_pos())
                if event.button ==1 and self.player_with_turn == self.user:
                    print str(pygame.mouse.get_pos())
                    card=self.drawer.obtain_zone(pygame.mouse.get_pos())
                    self.select_card(card)
            
            # Eventos de teclado
            if event.type == pygame.KEYDOWN:
                dic_func=self.down_func
            elif event.type == pygame.KEYUP:
                dic_func=self.up_func
                        
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if dic_func.has_key(event.key) and self.player_with_turn == self.user:
                    
                    if type(dic_func[event.key])==type([]):
                        tmp_fun=dic_func[event.key][0]
                        tmp_sco=dic_func[event.key][1] #scope:ambito:local,global
                        
                        if tmp_sco=="global":
                            #if self.user==self.pwt:
                            self.globaleventlist.append( str(tmp_fun)+","+str(self.user) )
                        else:
                            print eval(tmp_fun)

                        print self.globaleventlist

                    else:
                        dic_func[event.key]()
        
    def update(self):
        # Eventos de la lista
        for event in self.globaleventlist:
            string = event.split(",")
            string[-1] = "player=" + string[-1]
            function = string[0]
            args = ",".join(string[1:])
            eval(function + "(" + args + ")")
            if self.net:
                self.net.send(function+':'+args)
            del self.globaleventlist[self.globaleventlist.index(event)]
        
        if self.net:
                if self.player_with_turn != self.user:
                    # No es mi turno, tengo que esperar a que alguien
                    # envie algo
                    msg = self.net.read_non_blocking()
                    if msg:
                        print msg
                        sender, msg = msg.split('#')
                        if msg[0:3] == 'FUN':
                            print 'DEBUG ===========> ', msg
                            function, args = msg[4:].split(':')
                            eval(function + '(' + args + ')')

    def draw(self):
        pass
        
    def new_round(self):
        """Es llamada al crear el juego y cada vez que se empieza una nueva ronda"""
        self.app=self.core.get_app()
        self.round+=1
        for player in self.app.m['players'].values():
            del player[:]
        #del self.app.m['deckdraws'][:]
        self.app.m.clear
		
        for ideck in self.rules.deckdraws:
            
            self.add_deckdraw(Deck(id_deck=ideck["name"], cards=[ideck["numbers"],ideck["suits"]],visible=False,point=self.rules.points))
        
        self.rules.init_round()
        
    #seleccionar
    def select(self,n,player=-1):
        self.player=player
        self.player.select(n)
        try: self.rules.select()
        except AttributeError: pass
        self.show()
        
    def clear_selection(self,player=-1):
        self.player=player
        self.player.clear_selection_from_deck()
        try: self.rules.clear_selection()
        except AttributeError: pass
        self.show()
    
    #seleccionar con el raton
    def select_card(self,card,player=-1):
        self.player=player
        self.player.select_card(card)
        try: self.rules.select()
        except AttributeError: pass
        self.show()
        
    
    
    #entre mazos    
    def throw_cards(self,player=-1):
        self.player=player
        selection=self.player.get_selection_from_deck()                
        if self.throwable_selection(selection):#and self.p[self.pwt].clickable:
            self.player.send(self.playzone[self.playzone_active])
            self.throws.append(selection)
            try: self.rules.throw_cards(selection)
            except AttributeError: pass
            self.show()
    
    def throwable_selection(self,selection):
        try: r=self.rules.throwable_selection(selection)
        except AttributeError: r=True
        return r
    
    def draw_a_card(self,n=1,player=-1):
        self.player=player
        self.player.draw_a_card(self.deckdraws[0],n)
        try: self.rules.draw_a_card()
        except AttributeError: pass
        self.draw.show()
        
    def deal(self,n):
        self.deckdraws[0].deal(n,self.p)
        try: self.rules.deal()
        except AttributeError: pass
        self.show()
    
    #otras
    def pass_turn(self,player=-1):
        self.player=player
        self.pass_turns_counter+=1
        try: self.rules.pass_turn()
        except AttributeError: pass
        self.ending_turn(pass_turn=True)
        
    def end_turn(self,player=-1):
        self.player=player
        if self.terminable_turn:
            try: self.rules.end_turn()
            except AttributeError: pass
            self.ending_turn()
            
    def ending_turn(self,pass_turn=False):
        self.clear_selection()
        if not pass_turn:
            self.pass_turns_counter=0
        if self.clockwise_direction:
            self.player_with_turn+=1
        else:
            self.player_with_turn-=1
        if self.pwt==0:
            self.turn+=1
        self.player_with_turn%=len(self.p)
        self.player=self.p[self.pwt]
        try: self.rules.ending_turn()
        except AttributeError: pass
        try: irf = self.rules.is_round_finished()
        except AttributeError: irf = False
        if irf:
            try: self.rules.end_of_round()
            except AttributeError: pass
            self.new_round()
            
        else:           
            self.show()
            try: self.rules.new_turn()
            except AttributeError: pass
    
    def clear_playzone(self):
        del self.playzone[0].cards[:]
        
    def stick(self):
        pass#plantarse o retirarse TODO no puede estar bien, no es lo mismo no apostar mas que dejar el juego
        
    def discard(self,deckdiscard=None,player=-1):
        self.player=player
        #if self.p[self.pwt].clickable:
        if deckdiscard==None:
            deckdiscard=self.deckdiscard[self.deckdiscard_active]
        self.player.send(deckdiscard)
        self.show()
        
    #ordenar
    def sort_by_suit(self,player=-1):
        """ordena el mazo del jugador cuyo indice se pasa por argumentos, en caso de no indicar cual utilizara
    el jugador con el turno"""
        self.player=player
        self.player.sort_by_suit()
        self.show()
        
    def sort_by_number(self,player=-1):
        self.player=player
        self.player.sort_by_number()
        self.show()
        
    def sort_by_points(self,player=-1):
        self.player=player
        self.player.sort_by_points()
        self.show()
        
    def sort(self,by,player):
        if by=="suit":
            self.globaleventlist.append([self.user,"self.actions.sort_by_suit()"])
        elif by=="number":
            self.globaleventlist.append([self.user,"self.actions.sort_by_number()"])
        elif by=="points":
            self.globaleventlist.append([self.user,"self.actions.sort_by_points()"])
        
    def exit(self):
        self.exit()
    
    def showalt(self):
        if self.show_layer_alternative:
            self.show_layer_alternative = False
        else:
            self.show_layer_alternative = True
        self.show()

    def __getattr__(self, attr):
        if attr=="player":
            return self.p[self.p]
            
    def __setattr__(self, attr, value):
        if attr=="player" and value ==-1:
            try: self.__dict__["p"] = self.player_with_turn
            except AttributeError:pass
        elif attr=="player":
            self.__dict__["p"] = value
        else:
            self.__dict__[attr] = value
            
    #acciones para las pruebas       
    def prueba1(self):
        self.drawer.ancho *= 0.5
        pass
    def prueba2(self):
        pass
        
    def F(self,f=0):
        for player in self.players:
            for card in player.cards:
                card.setVisibility(False)
                
        if f!=10 and f<len(self.players):
            self.user=f
            self.players[f].visible=False
            
            for card in self.players[f].cards:
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
        
