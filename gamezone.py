import os
import sys
import pygame
import socket

from deck import Deck
from drawer import Drawer

import luarules


keys = {
    pygame.K_ESCAPE: "esc",
    pygame.K_LALT: "lalt",
    pygame.K_RALT: "ralt",
    pygame.K_LCTRL: "lctrl",
    pygame.K_RCTRL: "rctrl",
    pygame.K_LSHIFT: "lshift",
    pygame.K_RSHIFT: "rshift",
    pygame.K_LEFT: "left",
    pygame.K_UP: "up",
    pygame.K_RIGHT: "right",
    pygame.K_DOWN: "down",
    pygame.K_DELETE: "delete",
    pygame.K_BACKSPACE: "backspace",
    pygame.K_SPACE: "space",
    pygame.K_RETURN: "ret",
    pygame.K_F1: "F1",
    pygame.K_F2: "F2",
    pygame.K_F3: "F3",
    pygame.K_F4: "F4",
    pygame.K_F5: "F5",
    pygame.K_F6: "F6",
    pygame.K_F7: "F7",
    pygame.K_F8: "F8",
    pygame.K_F9: "F9",
    pygame.K_F10: "F10",
    pygame.K_F11: "F11",
    pygame.K_F12: "F12",
    pygame.K_F13: "F13",
    pygame.K_F14: "F14",
    pygame.K_F15: "F15",
}



class Gamezone(object):
    def __init__(self,rules=False,down_func={},up_func={}, netobj=None, players=[]):
        self.show_layer_alternative=False
        
        self._counter=0
        self.player_with_turn=0
        self.pass_turns_counter=0 

        
        self.keys_descriptions="Esc:Exit"
        self.down_func=down_func
        if not self.down_func.has_key(pygame.K_ESCAPE):
            self.down_func[pygame.K_ESCAPE]=sys.exit
        
        self.up_func=up_func
        self.clockwise_direction=True
        self.pass_turns_counter=0 # contador de turnos sin tiradas
        self.round=0
        self.turn=0 #TODO: vueltas k lleva la partida
        self.players=[]
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
        
        
        
        mode = "lua"
        if mode == "py":
            rules=__import__("rules").get_module(rules)
            self.rules=rules.Game(self)
        elif mode == "lua":
            self.rules = luarules.load(rules, {"getattr":getattr, "len":len, "game":self},
            {"deckdraw":lambda: self.deckdraws[0]})
        else:
            raise Exception("mode != [py|lua]")
        
        
        self.drawer=Drawer(self,caption=self.rules.caption)
        
        try: self.keys_descriptions=self.rules.keys_descriptions
        except AttributeError: pass
        
        for player in players:
            self.add_player(id_deck=player)
        if self.rules.playzone:
            self.add_playzone(id_deck="playzone",visible=True)
    
        
        
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
            visible = len(self.players)==self.user
                
        if clickable == None:
            clickable = len(self.players)==self.user
        
        if point:
            player=Deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable,point=point)
        else:
            player=Deck(id_deck=id_deck,cards=cards,visible=visible,maxcards=maxcards,clickable=clickable)

        self.players.append(player)
        self.player = self.players[self.player_with_turn]

    def __str__(self):
        r="_________GAME_________"
        r+="\n\n"+_("Draw Decks")+":"
        for deck in self.deckdraws:
            r+="\n    "+str(deck)
            
        r+="\n\n"+_("Player Decks")+":"
        for deck in self.players:
            r+="\n    "+str(deck)
            
        r+="\n\n"+_("Play Zone")+":"
        for deck in self.playzone:
            r+="\n    "+str(deck)
        r+="\n\n"+_("Selection")+":"
        r+="\n    "
        for card in self.players[self.user].selection:
            r+=" "+str(card)+""
        r+="\n\n"+_("Selection")+" ("+_("player with turn")+"):"
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
        #print self
    
    
    def __iter__(self):
        return iter([self.players, self.deckdraws, self.deckdiscard, self.deckpoints, self.playzone])


    # Bucle principal
    def init_bucle(self):
        self.clock = pygame.time.Clock()
        
        while True:
            self.clock.tick(5)
                
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
                    #print "boton" + str(event.button) + str(pygame.mouse.get_pos())
                    if event.button ==1 and self.player_with_turn == self.user:
                        #print str(pygame.mouse.get_pos())
                        card=self.drawer.obtain_zone(pygame.mouse.get_pos())
                        self.select_card(card)
                
                # Eventos de teclado
                if event.type == pygame.KEYDOWN:
                    dic_func=self.down_func
                elif event.type == pygame.KEYUP:
                    dic_func=self.up_func
                            
                if event.type == pygame.KEYDOWN:# or event.type == pygame.KEYUP:
                    key = repr(str(event.dict.get("unicode", "")))[1:-1]
                    key = repr(str(keys.get(event.key, key)))[1:-1]
                    if dic_func.has_key(key) and (True or self.player_with_turn == self.user): # "true or", para poder cambiar de jugador
                        

                        
                        if isinstance(dic_func[key], list):
                            tmp_fun=dic_func[key][0]
                            tmp_sco=dic_func[key][1] #scope:ambito:local,global
                            
                            if tmp_sco=="global":
                                #if self.user==self.pwt:
                                self.globaleventlist.append( str(tmp_fun)+","+str(self.user) )
                            else:
                                #print "tmp_fun: %s" % tmp_fun
                                eval("self."+tmp_fun)

                            #print "globalevenlist: %s" % self.globaleventlist

                        else:
                            dic_func[key]()


                # Eventos de la lista
                for event in self.globaleventlist:
                    func_args = event.split(",")
                    function = func_args[0]
                    args = func_args[1:]
                    #args[-1] = "player=" + args[-1]
                    getattr(self,function)(*args[:-1], player=int(args[-1]))
                    """
                    args[-1] = "player=" + args[-1]
                    args_ = ",".join(args)
                    eval("self.%s(%s)" % (function, args_))
                    
                    f = file("f.txt","a")
                    f.write(repr((function, args_, args)))
                    f.close()
                    """
                    if self.net:
                        self.net.send(function+':'+args)
                    del self.globaleventlist[self.globaleventlist.index(event)]
                    
                    
            if self.net:
                if self.player_with_turn != self.user:
                    # No es mi turno, tengo que esperar a que alguien
                    # envie algo
                    msg = self.net.read_non_blocking()
                    if msg:
                        #print msg
                        sender, msg = msg.split('#')
                        if msg[0:3] == 'FUN':
                            #print 'DEBUG ===========> ', msg
                            function, args = msg[4:].split(':')
                            eval(function + '(' + args + ')')

    def exit(self):
        sys.exit()
        
        
        
    def new_round(self):
        """Es llamada al crear el juego y cada vez que se empieza una nueva ronda"""
        self.round+=1
        for player in self.players:
            del player[:]
        del self.deckdraws[:]
        del self.deckdiscard[:]
        del self.deckpoints[:]
        for playzone in self.playzone:
            del playzone[:]
        del self.throws[:]
        for ideck in self.rules.deckdraws:
            self.add_deckdraw(Deck(id_deck=ideck['name'], cards=[ideck['numbers'],ideck['suits']],visible=False,point=self.rules.points))

        self.user = self.player_default
        self.player_with_turn=0
        
        self.rules.new_round()
     
    #seleccionar
    def select(self,n,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.select(n)
        self.rules.select()
        self.show()
        
    def clear_selection(self,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.clear_selection_from_deck()
        self.rules.clear_selection()
        self.show()
    
    #seleccionar con el raton
    def select_card(self,card,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.select_card(card)
        self.rules.select()
        self.show()
    
    #entre mazos    
    def throw_cards(self,player=-1):
        player = self.player if player == -1 else self.players[player]
        selection=player.get_selection_from_deck()
        if self.throwable_selection(selection):#and self.p[self.pwt].clickable:
            player.send(self.playzone[self.playzone_active])
            self.throws.append(selection)
            self.rules.throw_cards(selection)
            self.show()
    
    def throwable_selection(self,selection):
        r=self.rules.throwable_selection(selection)
        return r
    
    def draw_a_card(self,n=1,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.draw_a_card(self.deckdraws[0],n)
        self.rules.draw_a_card()
        self.show()
        
    def deal(self,n):
        self.deckdraws[0].deal(n,self.players)
        self.rules.deal()
        self.show()

    #otras
    def pass_turn(self,player=-1):
        #player = self.player if player == -1 else self.players[player]
        self.pass_turns_counter+=1
        self.rules.pass_turn()
        self.ending_turn(pass_turn=True)
        
    def end_turn(self,player=-1):
        player = self.player if player == -1 else self.players[player]
        if self.rules.terminable_turn():
            self.rules.end_turn()
            self.ending_turn()
            
    def ending_turn(self,pass_turn=False):
        self.clear_selection()
        if not pass_turn:
            self.pass_turns_counter=0
        if self.clockwise_direction:
            self.player_with_turn+= 1 
        else:
            self.player_with_turn-= 1 
        if self.pwt==0:
            self.turn+=1
        self.player_with_turn%=len(self.players)
        self.player=self.players[self.pwt]
        self.rules.ending_turn()
        if self.rules.is_round_finished():
            #print "\n"*10, "END OF ROUND", "\n"*10 
            self.rules.end_of_round()
            if self.rules.is_game_finished():
                self.rules.end_game()
            else:
                self.new_round()
        else:
            self.show()
            self.rules.new_turn()
            
    def clear_playzone(self):
        del self.playzone[0].cards[:]
        
    def stick(self):
        pass#plantarse o retirarse TODO no puede estar bien, no es lo mismo no apostar mas que dejar el juego
        
    def discard(self,deckdiscard=None,player=-1):
        player = self.player if player == -1 else self.players[player]
        #if self.p[self.pwt].clickable:
        if deckdiscard==None:
            deckdiscard=self.deckdiscard[self.deckdiscard_active]
        player.send(deckdiscard)
        self.show()
        
    #ordenar
    def sort_by_suit(self,player=-1):
        """ordena el mazo del jugador cuyo indice se pasa por argumentos, en caso de no indicar cual utilizara
    el jugador con el turno"""
        player = self.player if player == -1 else self.players[player]
        player.sort_by_suit()
        self.show()
        
    def sort_by_number(self,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.sort_by_number()
        self.show()
        
    def sort_by_points(self,player=-1):
        player = self.player if player == -1 else self.players[player]
        player.sort_by_points()
        self.show()
        
    def sort(self, by, player=-1):
        player = self.player if player == -1 else self.players[player]
        if by=="suit":
            self.globaleventlist.append("sort_by_suit,%s" % self.user)
        elif by=="number":
            self.globaleventlist.append("sort_by_number,%s" % self.user)
        elif by=="points":
            self.globaleventlist.append("sort_by_points,%s" % self.user)
        
    
    def showalt(self):
        if self.show_layer_alternative:
            self.show_layer_alternative = False
        else:
            self.show_layer_alternative = True
        self.show()
        
    def get_player(self):
        return self.players[self.player_with_turn]
    def set_player(self, value):
        if value ==-1:
            try: self.__dict__["p"] = self.player_with_turn
            except AttributeError:pass
        else:
            try: self.players[self.player_with_turn]=value
            except AttributeError: pass
    player = property(get_player, set_player, None, "I'm the 'player' property.")
    
    def get_pwt(self):
        return self.player_with_turn
    def set_pwt(self, value):
        self.player_with_turn=value
    pwt = property(get_pwt, set_pwt, None, "I'm the 'last_throw' property.")
    last_throw = property(lambda self: self.throws[len(self.throws)-1], None, None, "I'm the 'last_throw' property.")
    
    def __getitem__(self, key):
        return getattr(self, key)
            
    def __setitem__(self, key, val):
        return setattr(self, key, val)
            
    #acciones para las pruebas       
    def prueba1(self):
        print "prueba1"
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
        
    def toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()
