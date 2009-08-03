import deck
import card
import decks

class Player(object):
	def __init__(self, name="Nick"):
		self.name=name
		self.hand=deck.Deck()

	def clear(self):
		self.hand.clear()

class Game(object):
	def __init__(self):
		self.players=[]
		self.table=[]
		self.turn=0
		self.wins=[]
	
	def add_player(self, *args):
		self.players.append(Player(*args))

	def add_players(self, pl=[]):
		[self.add_player(i) for i in pl]
		
	def init_round(self):
		[p.clear() for p in self.players]
		self.table=[]
		self.turn=0
		self.wins=[]
		cards=decks.EspanyolaA7_JK()
		cards.shuffle()
		cards.deal(len(cards), [p.hand for p in self.players])

	def vision_of(self, n=-1):
		if n==-1:
			n=self.turn
		return [ self.players[n].hand, self.table,self.wins ]
		
	def no_vision_of(self, n=-1):
		if n==-1:
			n=self.turn
		return [self.players[i].hand for i in range(len(self.players)) if n!=i]
		
	def throw(self, n=-1):
		if n==-1:
			n=self.turn
		
		selfthrowable=self.throwable(n)
		if selfthrowable is True:
			self.table.append(deck.Deck())
			self.players[n].hand.send(self.table[-1])
			self.nextplayer()
		else:
			if selfthrowable:
				return selfthrowable
			else:
				return "No puedes tirar estas cartas"
			
	def nextplayer(self):
		self.turn+=1
		self.turn%=len(self.players)
			
	def throwable(self,n):
		#no te toca tirar
		if n != self.turn:
			return "Le toca tirar a %s, tu eres %s" % (self.turn+1, n+1)
		selection=self.players[n].hand.selection
		
		#Si no existe nada seleccionado
		if not selection:
			return "No has seleccionado ninguna carta"
		
		#las cartas de la selecion no son todas del mismo numero
		if len(selection)>1:
			number=selection[0].number
			for card in selection:
				if card.number!=number:
					return "las cartas deben ser todas del mismo numero"
					
		#no hay cartas en la mesa
		if not self.table:
			return True
		
		if len(self.table[-1]) != len(selection):
			return "debes echar el mismo numero de cartas que los otros jugadores"
		
		#es mayor que la ultima de la mesa
		if self.table[-1][0].number < selection[0]:
			return True
		else:
			return "Tus cartas han de superar a las de la mesa"
		

class PlayerController(object):
	def __init__(self, controller, n):
		self.controller=controller
		self.n=n
		self.player=self.controller.game.players[self.n]
		
	def vision(self):
		return self.controller.game.vision_of(self.n)
		
	def no_vision(self):
		return self.controller.game.no_vision_of(self.n)
		
	def throw(self):
		return self.controller.game.throw(self.n)
		
	def sort_by_number(self):
		self.player.hand.sort_by_number()
	
	def select(self,card):
		self.player.hand.select(card)
		
	def select_n(self,n):
		self.select(self.player.hand[(n-1)%len(self.player.hand)])
		
class ControllerGame(object):
	def __init__(self,game):
		self.game=game
	
	def get_player_controller(self, n):
		return PlayerController(self,n)
	
		
		
if __name__ == "__main__":
	import os
	g=Game()
	cg=ControllerGame(g)
	g.add_players(['Manolo', 'Nick', 'John', 'Stan'])
	g.init_round()
	
	pc=cg.get_player_controller(0)
	
	sms=""
	def p():
		os.system('cls')
		
		pc.sort_by_number()
		vision=pc.vision()
		novision=pc.no_vision()
	
		print 
		print sms
		print
		
		print "Estas son tus cartas:"
		
		s = ""
		for num,card in enumerate(vision[0]):
			s+= "%s:%s " % (num+1, card)
		print s
		#print " ".join(map(str,vision[0]))
		
		for n,dck in enumerate(novision):
			print
			print "Estas son las cartas del jugador %s:" % (n+2)
			print " ".join(("# " for d in dck))
		
		print
		print "Estas es la mesa:"
		print " ".join(map(str,vision[1]))
		print
		print "Estos son los que ya terminaron:"
		print " ".join(map(str,vision[2]))
		return raw_input('Num.:Seleccionar una carta. T:Lanzar. E:Salir.\n')
	
	endgame = False
	while not endgame:
		endturn = False
		while not endturn:
			foo = p()
			sms = ""
			if foo in ('t','T'):
				sms = pc.throw()
				if sms is None:
					sms = ""
					endturn=True
					
			elif foo.isdigit():
				pc.select_n(int(foo))
			
			elif foo.startswith('change:'):
				n = foo[len('change:'):]
				if n.isdigit():
					sms = 'cambiado al jugador: %s' % n
					pc = cg.get_player_controller(int(n)-1)
			
			elif foo in ('e','E'):
				endturn = True
				endgame = True