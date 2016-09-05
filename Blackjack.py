# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
	def __init__(self, suit, rank):
		if (suit in SUITS) and (rank in RANKS):
			self.suit = suit
			self.rank = rank
		else:
			self.suit = None
			self.rank = None
			print "Invalid card: ", suit, rank

	def __str__(self):
		return self.suit + self.rank

	def get_suit(self):
		return self.suit

	def get_rank(self):
		return self.rank

	def draw(self, canvas, pos):
		card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
					CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
		canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

	def draw_card_back(self, canvas, pos):
		card_loc = (CARD_CENTER[0], 
					CARD_CENTER[1])
		canvas.draw_image(card_back, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
		
# define hand class
class Hand:
	def __init__(self):
		#pass	# create Hand object
		self.cards = []
		self.hasAce = False

	def __str__(self):
		#pass	# return a string representation of a hand
		hand_str = ''
		for i in xrange(len(self.cards)):
			hand_str = hand_str+','+self.cards[i].__str__()
		print hand_str
		return hand_str

	def add_card(self, card):
		#pass	# add a card object to a hand
		self.cards.append(card)
		print card.__str__()
		if(card.get_rank()=='A'):
			self.hasAce = True

	def get_value(self):
		# count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
		# pass	# compute the value of the hand, see Blackjack video
		val= 0
		for i in xrange(len(self.cards)):
			val = val + VALUES[self.cards[i].get_rank()]
		if(self.hasAce==False):
			return val
		else:
			if(val+10<=21):
				return val+10
			else:
				return val
		
	def draw(self, canvas, pos):
		#pass	# draw a hand on the canvas, use the draw method for cards
		for i in xrange(len(self.cards)):
			self.cards[i].draw(canvas, [pos[0]+i*(CARD_SIZE[0]+10),pos[1]])

	def get_first_card(self):
		if(len(self.cards)>1):
			return self.cards[0]
		return None

# define deck class 
class Deck:
	def __init__(self):
		# pass	# create a Deck object
		self.cards = []
		for i in xrange(len(SUITS)):
			for j in xrange(len(RANKS)):
				self.cards.append(Card(SUITS[i],RANKS[j]))
		self.shuffle()

	def shuffle(self):
		# shuffle the deck 
		# pass    # use random.shuffle()
		random.shuffle(self.cards)

	def deal_card(self):
		# pass	# deal a card object from the deck
		# card=self.cards[0]
		return self.cards.pop()

	def __str__(self):
		# pass	# return a string representing the deck
		deck_str = ''
		for i in xrange(len(self.cards)):
			deck_str = hand_str+','+self.cards[i].__str__()
		print deck_str
		return deck_str


#define event handlers for buttons
def deal():
	global outcome, in_play

	# your code goes here
	global dealer_hand,player_hand,deck
	dealer_hand = Hand()
	player_hand = Hand()
	deck = Deck()
	outcome = ''
	
	in_play = True
	for i in xrange(2):
		hit()
	stand()

def hit():
	# pass	# replace with your code below
	global outcome, in_play,score

	# your code goes here
	global dealer_hand,player_hand,deck
	if(in_play):
		card = deck.deal_card()
		player_hand.add_card(card)
		if(player_hand.get_value()>21):
			in_play = False
			outcome = "Dealer win"
			score-=1
 
	# if the hand is in play, hit the player
   
	# if busted, assign a message to outcome, update in_play and score
	   
def stand():
	# pass	# replace with your code below
	global outcome, in_play,score

	# your code goes here
	global dealer_hand,player_hand,deck
	if(in_play):
		while(dealer_hand.get_value()<17):
			card = deck.deal_card()
			dealer_hand.add_card(card)
			if(dealer_hand.get_value()>=17):				
				return

		if(dealer_hand.get_value()>21):
			outcome = "Player win"
			score+=1
		elif(dealer_hand.get_value()>player_hand.get_value()):
			outcome = "dealer win"
			score-=1
		else:
			outcome = "Player win"
			score+=1
		in_play = False

	# if hand is in play, repeatedly hit dealer until his hand has value 17 or more

	# assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
	# test to make sure that card.draw works, replace with your code below
	
	# card = Card("S", "A")
	# card.draw(canvas, [300, 300])
	canvas.draw_text("dealer hand", (50, 180), 30, "Black")
	canvas.draw_text("player hand", (50, 380), 30, "Black")
	canvas.draw_text(outcome, (250, 380), 30, "Black")
	canvas.draw_text("score: " + str(score), (450, 100), 30, "Black")
	dealer_hand.draw(canvas,[100, 200])
	player_hand.draw(canvas,[100, 400])
	if(in_play):
		first_card = dealer_hand.get_first_card()
		first_card.draw_card_back(canvas,[100, 200])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric