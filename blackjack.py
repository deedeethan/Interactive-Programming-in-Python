# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (73, 98)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize global variables
deck = []
in_play = False
outcome = ""
prompt = "Hit or stand?"
score = 0

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            print "Invalid card: ", self.suit, self.rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(self.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(self.suit)))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_SIZE[0] / 2, pos[1] + CARD_SIZE[1] / 2], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.num_cards = 0
        self.value = 0

    def __str__(self):
        card = ""
        s = "hand contains"
        for c in self.cards:
            card = str(c)
            s += ' ' + str(card)
        return s

    def add_card(self, card):
        self.num_cards += 1
        self.cards.append(card)

    # count aces as 1 if the hand has an ace, then add 10 to hand value if don't bust
    def get_value(self):
        self.value = 0
        c = 0
        while c < len(self.cards):  # adds 1 for aces
            r = self.cards[c].rank
            v = VALUES[r]
            self.value += v
            c += 1

        for n in self.cards:   # goes back to add 10 for aces if not bust
            if n.rank == 'A':
                if self.value + 10 <= 21:
                    self.value += 10

        return self.value

    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False

    def draw(self, canvas, p):
        n = 0
        for c in self.cards:
            card_loc = (CARD_SIZE[0] * (0.5 + RANKS.index(c.rank)), CARD_SIZE[1] * (0.5 + SUITS.index(c.suit)))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [p[0] + CARD_SIZE[0]/2 + + n*100, p[1] + CARD_SIZE[1]/2], CARD_SIZE)
            n += 1

# define deck class
class Deck:
    def __init__(self):
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s,r))

    def __str__(self):
        card = ""
        s = "Deck contains"
        for c in self.cards:
            card = str(c)
            s += ' ' + str(card)
        return s + str(len(self.cards))

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        c = self.cards[-1]
        self.cards.remove(c)
        return c

# define callbacks for buttons
def deal():
    global deck, outcome, prompt, in_play, score, dealer_hand, player_hand

    if in_play:
        outcome = "You lose."
        prompt = "New deal?"
        in_play = False
        score -= 1
    else:
        deck = Deck()
        deck.shuffle()
        dealer_hand = Hand()
        player_hand = Hand()

        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())

        outcome = ""
        prompt = "Hit or stand?"
        in_play = True

def hit():
    global outcome, prompt, in_play, score, player_hand

    # if the hand is in play, hit the player
    if in_play and player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        prompt = "Hit or stand?"

    # if busted, assign an message to outcome, update in_play and score
    if player_hand.busted():
        outcome = "Busted! You lose."
        prompt = "New deal?"
        in_play = False
        score -= 1

def stand():
    global outcome, prompt, in_play, score, dealer_hand

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
    if dealer_hand.busted():
        outcome = "Dealer has busted. You win!"
        prompt = "New deal?"
        in_play = False
        score += 1
    elif player_hand.busted():
        outcome = "Busted! You lose."
        prompt = "New deal?"
        in_play = False
        score -= 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value():
            outcome = "Dealer wins."
            score -= 1
        else:
            outcome = "You win!"
            score += 1
        prompt = "New deal?"
        in_play = False

def draw(canvas):
    canvas.draw_text("Blackjack", [70,120], 50, "Blue")
    canvas.draw_text("Score " + str(score), [400,120], 30, "White")
    canvas.draw_text("Dealer", [80,200], 30, "Black")
    canvas.draw_text(outcome, [290,200], 26, "Black")
    canvas.draw_text("Player", [80,400], 30, "Black")
    canvas.draw_text(prompt, [290,400], 26, "Black")

    if in_play:
        dealer_hand.draw(canvas, [80,220])
        card_loc = (71/2, 96/2)
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [116, 269], CARD_BACK_SIZE)
        player_hand.draw(canvas, [80,420])
    else:
        dealer_hand.draw(canvas, [80,220])
        player_hand.draw(canvas, [80,420])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 150)
frame.add_button("Hit",  hit, 150)
frame.add_button("Stand", stand, 150)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()

