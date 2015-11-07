# implementation of card game - Memory

import simplegui
import random

turns = 0
first_click = -1
second_click = -1

# helper function to initialize globals
def new_game():
    global cards, turns, exposed, pos_num, pos_card1, pos_card2, pos_line1, pos_line2
    turns = 0
    label.set_text('Turns = ' + str(turns))
    match = range(0,8)
    cards = range(0,8) + match
    random.shuffle(cards)

    exposed = [False for i in range(16)]

    # list of positions of numbers
    x = 20
    pos_num = [[x + 50*n, 60] for n in range(16)]

    # lists of positions of cards
    x = 25
    pos_card1 = [[x + 50*n, 0] for n in range(16)]

    x = 25
    pos_card2 = [[x + 50*n, 100] for n in range(16)]

    # lists of positions of lines
    x = 50
    pos_line1 = [[x + 50*n, 0] for n in range(16)]

    x = 50
    pos_line2 = [[x + 50*n, 100] for n in range(16)]

# define event handlers
def mouseclick(pos):
    global turns, first_click, second_click
    num = pos[0]//50
    if exposed[num] == True:
        pass
    else:
        if first_click == -1:
            first_click = num
            exposed[num] = True
        elif second_click == -1:
            second_click = num
            exposed[num] = True
            turns += 1
            label.set_text('Turns = ' + str(turns))
        else:
            if cards[first_click] == cards[second_click]:
                first_click = num
                exposed[num] = True
                second_click = -1
            else:
                exposed[first_click] = False
                exposed[second_click] = False
                first_click = num
                exposed[num] = True
                second_click = -1

# cards are logically 50x100 pixels in size
def draw(canvas):
    for n in range(16):
        if exposed[n] == True:
            canvas.draw_text(str(cards[n]), pos_num[n], 35, "White")
        else:
            canvas.draw_line(pos_card1[n], pos_card2[n], 50, "Green")
            canvas.draw_line(pos_line1[n], pos_line2[n], 2, "White")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

