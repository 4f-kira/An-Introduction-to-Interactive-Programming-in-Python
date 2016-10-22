# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global L,state,exposed_flag,turns
    turns = 0
    label.set_text("Turns = "+str(turns))
    exposed_flag = [0]*16
    state = 0
    L1 = range(8)+range(8)
    random.shuffle(L1)
    L = L1

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state,turns,exposed_flag,exposed_card1,exposed_card2
    selected_card = pos[0] // 50
    if exposed_flag[selected_card] == 0 :
        exposed_flag[selected_card] = 1
        if state == 0:
            state = 1
            exposed_card1 = selected_card
        elif state == 1:
            state = 2
            turns += 1
            label.set_text("Turns = "+str(turns))
            exposed_card2 = selected_card
        else:
            state = 1
            if not L[exposed_card1] is L[exposed_card2] :
                exposed_flag[exposed_card2] = 0
                exposed_flag[exposed_card1] = 0
            exposed_card1 = selected_card

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    text_pos = 5
    text_num = 0
    for x in L :
        if exposed_flag[text_num] == 1 :
            canvas.draw_text(str(x), (text_pos, 80), 75, 'White')
        else :
            canvas.draw_line((text_pos-4, 50), (text_pos+44, 50),100, 'Red')
        text_pos += 50
        text_num += 1
            

    
    
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric