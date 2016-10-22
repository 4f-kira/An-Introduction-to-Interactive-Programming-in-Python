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
score = 10

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

        
def change2str(s) :
    string = ''
    for i in range(len(s)):
        string += str(s[i])+' '
    return string

# define hand class
class Hand:
    def __init__(self):
        self.hand_card = []
        # create Hand object

    def __str__(self):        
        return 'Hand contains '+ change2str(self.hand_card)
        # return a string representation of a hand

    def add_card(self, card):
        self.hand_card.append(card)
        # add a card object to a hand  

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        num = ''
        for i in range(len(self.hand_card)):
            num += self.hand_card[i].get_rank()
        point = 0
        for x in num:
            point += VALUES[x]       
        if ('A' in num) and (point < 12):
            point += 10
        return point    
        # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand_card)):
            self.hand_card[i].draw(canvas,[pos[0]+i*72,pos[1]])
        # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.card = [ Card(x,y) for x in SUITS for y in RANKS]
        # create a Deck object

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card)
        # use random.shuffle()

    def deal_card(self):
        return self.card.pop(-1)
        # deal a card object from the deck
    
    def __str__(self):     
        return 'Deck contains '+ change2str(self.card)
        # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play,p_hand,g_deck,d_hand,score
    # your code goes here
    if in_play :
        score -= 1
    outcome = 'Hit or stand?'
    g_deck = Deck()
    g_deck.shuffle()
    p_hand = Hand()
    d_hand = Hand()
    p_hand.add_card(g_deck.deal_card())
    p_hand.add_card(g_deck.deal_card())
    d_hand.add_card(g_deck.deal_card())
    d_hand.add_card(g_deck.deal_card())
    in_play = True

def hit():
    # replace with your code below
    global outcome, in_play, score
    if not in_play:
        return
    # if the hand is in play, hit the player
    p_hand.add_card(g_deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if p_hand.get_value() > 21:
        in_play = False
        score -= 1
        outcome = "You have busted"
    #print p_hand
    #print p_hand.get_value()
       
def stand():
    # replace with your code below
    global outcome, in_play, score
    if not in_play:
        return
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while d_hand.get_value() < 17:
        d_hand.add_card(g_deck.deal_card())
        #print d_hand.get_value()
    # assign a message to outcome, update in_play and score
    in_play = False 
    if d_hand.get_value() > 21 or p_hand.get_value() > d_hand.get_value():
        score += 1
        outcome = 'You win !!'
    else :
        score -= 1
        outcome = 'You lose ~~'

        
        
def mouseclick(pos):
    if pos[0]>10 and pos[0]<80 and pos[1]>335 and pos[1]<365:
        deal()
    elif pos[0]>85 and pos[0]<155 and pos[1]>335 and pos[1]<365:
        hit()
    elif pos[0]>160 and pos[0]<230 and pos[1]>335 and pos[1]<365:
        stand()
    
    
    
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text( outcome , [75,300], 30, "White","sans-serif")
    canvas.draw_text( 'DouBi Blackjack' , [100,200], 50, "Blue","sans-serif")
    canvas.draw_text( 'GOLD '+str(score) , [450,100], 25, "Yellow","sans-serif")
    d_hand.draw(canvas, [10, 10])    
    p_hand.draw(canvas, [10, 500])
    if in_play :
        canvas.draw_image(card_back,CARD_CENTER, CARD_SIZE, [10 + CARD_CENTER[0], 10 + CARD_CENTER[1]], CARD_SIZE)
    button = ["Deal","  Hit","Stand"]
    for i in range(0,3):
        canvas.draw_line((10+i*75, 350), (80+i*75, 350), 30, 'Black')
        canvas.draw_text(button[i] , [12+i*75,360], 25, "White","sans-serif")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick)

# get things rolling
deal()
frame.start()


# remember to review the gradic rubric