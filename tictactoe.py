
import simplegui

turn = 1
sign = ""
point = [0,0]
game_over = False
values = {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:''}
empty = [True for i in range(9)]
outcome = "Fancy a game of Tic-Tac-Toe?"

# Handler for mouse click
def mouse_handler(position):
    global turn, sign, point, values, outcome
    if turn%2 == 1:
        sign = "O"
        outcome = "X's turn."
    else:
        sign = "X"
        outcome = "O's turn."
    turn += 1
    label.set_text(outcome)

    if position[1] < 100:
        if position[0] < 100:
            point = [30,70]
            values[1] = sign
            empty[0] = False
        elif position[0] < 200:
            point = [130,70]
            values[2] = sign
            empty[1] = False
        elif position[0] < 300:
            point = [230,70]
            values[3] = sign
            empty[2] = False
    elif position[1] < 200:
        if position[0] < 100:
            point = [30,170]
            values[4] = sign
            empty[3] = False
        elif position[0] < 200:
            point = [130,170]
            values[5] = sign
            empty[4] = False
        elif position[0] < 300:
            point = [230,170]
            values[6] = sign
            empty[5] = False
    elif position[1] < 300:
        if position[0] < 100:
            point = [30,270]
            values[7] = sign
            empty[6] = False
        elif position[0] < 200:
            point = [130,270]
            values[8] = sign
            empty[7] = False
        elif position[0] < 300:
            point = [230,270]
            values[9] = sign
            empty[8] = False
    get_winner()

def new_game():
    global game_over, turn, sign, point, outcome, values
    game_over = False
    turn = 1
    sign = ""
    point = [0,0]
    values = {1:'', 2:'', 3:'', 4:'', 5:'', 6:'', 7:'', 8:'', 9:''}
    outcome = "Fancy a game of Tic-Tac-Toe?"
    label.set_text(outcome)

def get_winner():
    global outcome
    for n in range(1,8):
        if empty[n] == False:
            if values[n] == values[n+1] == values[n+2]:
                outcome = values[n] + " wins horizontally!"
                game_over = True
    for n in range(1,4):
        if empty[n] == False:
            if values[n] == values[n+3] == values[n+6]:
                outcome = values[n] + " wins vertically!"
                game_over = True
    if empty[n] == False:
        if values[1] == values[5] == values[9]:
            outcome = values[n] + " wins diagonally!"
            game_over = True
        if values[3] == values[5] == values[7]:
            outcome = values[n] + " wins diagonally!"
            game_over = True
    label.set_text(outcome)

# Handler to draw on canvas
def draw(canvas):
    if game_over == False:
        for n in range(9):
            if empty[n] == False:
                # draws only one sign at a time bc point is changed with each click
                canvas.draw_text(sign, point, 60, "Red")
    canvas.draw_line([100,0], [100,300], 5, "White")
    canvas.draw_line([200,0], [200,300], 5, "White")
    canvas.draw_line([0,100], [300,100], 5, "White")
    canvas.draw_line([0,200], [300,200], 5, "White")

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Tic-Tac-Toe", 300, 300)
label = frame.add_label("Fancy a game of Tic-Tac-Toe?")
frame.add_button("New game", new_game)
frame.set_mouseclick_handler(mouse_handler)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()

