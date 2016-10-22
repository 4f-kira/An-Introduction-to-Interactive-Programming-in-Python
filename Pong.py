# Implementation of classic arcade game Pong

import simplegui
import random
import math
# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle_vel = 8
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = 200.0
paddle2_pos = 200.0
ball_pos = [ WIDTH/2 , HEIGHT/2 ]
ball_vel = [ 0.0 , 0.0 ]
pause_tag = True
game_time = 0
ai_mode = 'off'
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, game_time # these are vectors stored as lists
    ball_pos = [ WIDTH/2 , HEIGHT/2 ]
    if direction == 1 : # 1 = left
        ball_vel[0] = -2.0 
    elif direction == 0 :
        ball_vel[0] = 2.0 # 0 = right
    ball_vel[1] = random.randrange(-3, 0)
    game_time = 0

#Pause
def pause():
    global pause_tag
    pause_tag = not pause_tag 
    
def start():
    global pause_tag
    pause_tag = False
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel  # these are numbers
    global score1, score2 , pause_tag # these are ints
    pause_tag = True
    score1 = score2 = 0
    paddle1_pos = 200
    paddle2_pos = 200
    ball_pos = [ WIDTH/2 , HEIGHT/2 ]
    spawn_ball(random.randrange(0, 2))
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_text(format(game_time), [280,380], 20, "White")
    canvas.draw_text( 'AI:'+ai_mode , (500,380), 10, 'White')
    
    if not pause_tag : 
    # update ball
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    # update paddle's vertical position, keep paddle on the screen
        if (paddle1_pos <= PAD_HEIGHT/2 and paddle1_vel == -paddle_vel) or \
            (paddle1_pos >= HEIGHT-PAD_HEIGHT/2 and paddle1_vel == paddle_vel) :
            pass
        else :
            paddle1_pos += paddle1_vel
        if ai_mode == 'off' :    
            if (paddle2_pos <= PAD_HEIGHT/2 and paddle2_vel == -paddle_vel) or \
            (paddle2_pos >= HEIGHT-PAD_HEIGHT/2 and paddle2_vel == paddle_vel) :
                pass
            else :
                paddle2_pos += paddle2_vel
        else :
            if ball_vel[0] > 0 :
                ai()
                
                   
    # determine whether paddle and ball collide    
    if (ball_pos[1]-BALL_RADIUS) <= 0 or (ball_pos[1]+BALL_RADIUS) >= HEIGHT :
        ball_vel[1] = -ball_vel[1]
    if (ball_pos[0]-BALL_RADIUS) <= PAD_WIDTH or (ball_pos[0]+BALL_RADIUS) >= WIDTH - PAD_WIDTH :
        if ball_pos[0] <= 300 :
            if ball_pos[1] >= (paddle1_pos - PAD_HEIGHT/2) and  ball_pos[1] <= (paddle1_pos + PAD_HEIGHT/2):
                 ball_vel[0] = -(ball_vel[0]-1) 
            else :
                score2 += 1
                spawn_ball(0)  
        else :
            if ball_pos[1] >= (paddle2_pos - PAD_HEIGHT/2) and  ball_pos[1] <= (paddle2_pos + PAD_HEIGHT/2):
                ball_vel[0] = -(ball_vel[0]+1)
            else :
                score1 += 1
                spawn_ball(1) 
                
    # draw paddles
    canvas.draw_line( [ 0 , paddle1_pos ] ,[ 8 , paddle1_pos ], PAD_HEIGHT , "White")
    canvas.draw_line( [ 592 , paddle2_pos ] ,[ 600 , paddle2_pos ], PAD_HEIGHT , "White")
    # draw ball
    canvas.draw_circle( [ball_pos[0], ball_pos[1] ], BALL_RADIUS, 1, 'Yellow', 'Orange')
    # draw scores
    canvas.draw_text( str(score1) , (240,100), 50, 'Red')
    canvas.draw_text( str(score2) , (335,100), 50, 'Red')


def ai():
    global ball_pos, ball_vel, paddle2_pos
    ai_pos = int((ball_vel[1]/ball_vel[0])*(592-ball_pos[0])+ball_pos[1]) #
    ai_vel = 2
    if ai_mode == 'normal' : 
        if ai_pos <= 40:
            ai_pos = 40
        elif ai_pos >= 360 :
            ai_pos = 360
        if paddle2_pos > ai_pos :
            paddle2_pos -= ai_vel
        elif paddle2_pos < ai_pos :
            paddle2_pos += ai_vel     
    if ai_mode == 'medium' :
        if abs(ai_pos) <= 40 :
            ai_pos = 40 
        if abs(ai_pos) > 40 and abs(ai_pos) < 360 :
            ai_pos = abs(ai_pos)
        elif ai_pos >= 360 :
            ai_pos = 360
        if paddle2_pos > ai_pos :
            paddle2_pos -= ai_vel*2
        elif paddle2_pos < ai_pos :
            paddle2_pos += ai_vel*2
    if ai_mode == 'hard': 
        if ai_pos <= 0 or ai_pos >= 400:
            ai_pos = 200
        paddle2_pos = ai_pos
        
        
        
        
def set_normal():
    global ai_mode
    ai_mode = 'normal'
    new_game()
    
def set_medium():
    global ai_mode
    ai_mode = 'medium'
    new_game()
    
def set_hard():
    global ai_mode
    ai_mode = 'hard'
    new_game()
    
def ai_exit():
    global ai_mode
    ai_mode = 'off'
    new_game()
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -paddle_vel
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = paddle_vel
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = -paddle_vel
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = paddle_vel  
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0     

def tick():
    global game_time
    if not pause_tag :
        game_time += 1
                   
def format(t):
    A = t // 600
    B = t % 600 // 100
    C = t % 100 // 10
    return str(A)+':'+str(B)+str(C)      
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New game", new_game, 100)
frame.add_button("GO!!", start, 100)
frame.add_button("Pause", pause, 100)
frame.add_button("Noraml_AI", set_normal, 100)
frame.add_button("Medium_AI", set_medium, 100)
frame.add_button("Hard_AI", set_hard, 100)
frame.add_button("AI_MODE_Exit", ai_exit, 100)
timer = simplegui.create_timer(100, tick)
# start frame
new_game()
frame.start()
timer.start()