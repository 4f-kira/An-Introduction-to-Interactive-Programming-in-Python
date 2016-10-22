# template for "Stopwacth: The Game"
import simplegui

# define global variables
cu_time = 0  #current time
success_n = 0  #success number
attempts_n = 0  #attempts number
P1 = 0  #Player1 score
P2 = 0  #Player2 score
vs_mode = 0
winner = ' '

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t // 600
    B = t % 600 // 100
    C = t % 100 // 10
    D = t % 10
    return str(A)+':'+str(B)+str(C)+'.'+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    if not timer.is_running():
        return
    global cu_time,success_n,attempts_n
    attempts_n += 1
    timer.stop()
    if cu_time % 10 == 0:
        success_n +=1
        
def reset():
    global cu_time,success_n,attempts_n,P1,P2,winner
    timer.stop()
    P2 = P1 = success_n = attempts_n = cu_time = 0
    winner = ' '

# define event handler for timer with 0.1 sec interval
def tick():
    global P1,P2,winner,cu_time
    if (P1 > 11 and P2 > 11) or (P1 < -11 and P2 < -11) :
        winner = 'null'
        stop()
    elif P1 > 11 or P2 < -11 :
        winner = 'P1'
        stop()
    elif P2 > 11 or P1 < -11 :
        winner = 'P2'
        stop()
    cu_time += 1
    
def mode_c():
    global vs_mode
    reset()
    vs_mode = not vs_mode
    
# define draw handler
def draw(canvas):
    global cu_time,success_n,attempts_n,P1,P2
    if vs_mode :
        canvas.draw_text("P1 points:"+str(P1)+'      press A', [30,30], 20, "Red")
        canvas.draw_text("P2 points:"+str(P2)+'      press L', [30,270], 20, "Red")
        canvas.draw_text('success +3   fail -1', [75,100], 15, "Yellow")
        if winner == ' ' :
            canvas.draw_text(format(cu_time), [75,150], 50, "White")
        elif winner == 'null' :
            canvas.draw_text('Draw~~', [75,150], 50, "White")
        else :
            canvas.draw_text(winner+' win!!', [75,150], 50, "White")
    else :
        canvas.draw_text(format(cu_time), [75,150], 50, "White")
        canvas.draw_text(str(success_n)+'/'+str(attempts_n), [200,30], 25, "White")

def key_handler(key):
    global cu_time,success_n,attempts_n,P1,P2,vs_mode
    if not timer.is_running():
        return
    elif key == simplegui.KEY_MAP['a']:
        if cu_time % 10 == 0 :
            P1 = P1 + 3
        else :
            P1 = P1 - 1
    elif key == simplegui.KEY_MAP['l']:
        if cu_time % 10 == 0 :
            P2 = P2 + 3
        else :
            P2 = P2 - 1
       
    
# create frame
frame = simplegui.create_frame('Stopwacu_timeh: The Game',300,300)
frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)
frame.add_button("Change Mode", mode_c, 100)
frame.add_label('2P MODE : One player achieves more than 11 points , or below -11 points , Game Over.')
# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
frame.set_keydown_handler(key_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
