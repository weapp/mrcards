import deck
import card

def EspanyolaA7_JK():
	nums=range(2,8)
	nums.extend(['J','Q','K','A'])
	
	nums=range(1,10)
	suits=['oro','bastos','espadas','copas']
	suits=['O','B','E','C']
	return deck.Deck([card.Card(number=num, suit=suit, visible=True) for num in nums for suit in suits])
	