# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # vectors stored as lists

    ball_pos = [WIDTH/2, HEIGHT/2]
    v = random.randrange(1, 5)

    if direction == RIGHT:
        ball_vel = [v, -v]
    elif direction == LEFT:
        ball_vel = [-v, -v]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # numbers
    global score1, score2  # ints

    spawn_ball(RIGHT)
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel

    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:  # left collision
        if (paddle2_pos <= ball_pos[1] <= (paddle2_pos + 2*HALF_PAD_HEIGHT)):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(RIGHT)
            score1 += 1

    elif ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:  # right collision
        if (paddle1_pos <= ball_pos[1] <= (paddle1_pos + 2*HALF_PAD_HEIGHT)):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] *= 1.1
        else:
            spawn_ball(LEFT)
            score2 += 1

    elif ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:  # bottom collision
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] <= BALL_RADIUS:  # top collision
        ball_vel[1] = - ball_vel[1]

    # draw ball
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = HEIGHT/2 - HALF_PAD_HEIGHT # top left corner of paddle
    paddle2_pos = HEIGHT/2 - HALF_PAD_HEIGHT

    if paddle1_pos + paddle1_vel > 0: # this works
        paddle1_pos += paddle1_vel
    elif paddle1_pos + paddle1_vel < 0:
        paddle1_pos = 0
    elif paddle1_pos + paddle1_vel < HEIGHT - PAD_HEIGHT:  # this doesn't
        paddle1_pos += paddle1_vel
    elif paddle1_pos + paddle1_vel > HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT

    if paddle2_pos + paddle2_vel > 0:
        paddle2_pos += paddle2_vel
    elif paddle2_pos + paddle2_vel < 0:
        paddle2_pos = 0
    elif paddle2_pos + paddle2_vel < HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    elif paddle2_pos + paddle2_vel > HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT

    # draw paddles
    c.draw_line([2, paddle2_pos], [2, paddle2_pos + PAD_HEIGHT], 10, "White")
    c.draw_line([596, paddle1_pos], [596, paddle1_pos + PAD_HEIGHT], 10, "White")

    # draw scores
    c.draw_text(str(score1), [430,100], 60, "White")
    c.draw_text(str(score2), [140,100], 60, "White")

def keydown(key):
    global paddle1_vel, paddle2_vel
    v = 20
    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel -= v
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel += v
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel -= v
    elif key == simplegui.KEY_MAP["down"]:
        paddle1_vel += v

def keyup(key):
    # This doesn't work either.
    global paddle1_vel, paddle2_vel
    v = 0
    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel += v
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel -= v
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel += v
    elif key == simplegui.KEY_MAP["down"]:
        paddle1_vel -= v

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)

# start frame
new_game()
frame.start()
