# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import math
import random
game_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    print "\nNew game. Range is [0,"+str(game_range)+")"
    global retry_times
    retry_times = int(math.log(game_range,2))+1
    print "Number of remaining guesses is",retry_times
    global secret_num
    secret_num = random.randrange(0,game_range)
    global x
    global y
    x = 0
    y = game_range
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global game_range
    game_range  = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global game_range
    game_range = 1000
    new_game()
    
def rangeX(xxx):
    if xxx.isdigit() == False :
        print '\n Please input a digit!!'
        return
    global game_range
    game_range = int(xxx)
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    if guess.isdigit() == False :
        print '\n Please input a digit!!'
        return
    global retry_times
    global secret_num
    global x
    global y
    retry_times -= 1
    print '\nGuess was',guess
    print 'Number of remaining guesses is',retry_times
    if retry_times > 0 :        
        if int(guess) > secret_num :
            print 'Lower!'
            y = int(guess)
        elif int(guess) < secret_num :
            print 'Higher!'
            x = int(guess)
        else :
            print 'Correct!!!!!!!!!!!\n'
            new_game()
    else :
        if int(guess) == secret_num :
            print 'Correct!!!!!!!!!!!\n'
            new_game()
        else :
            print u'(ノ＝Д＝)ノ┻━┻ Game over~','The correct number is',secret_num,'\n'
            new_game()

# auto solve
def auto():
    global x
    global y
    a = int((y-x)/2) + x
    #print '\nrange is ['+str(x)+','+str(y)+']'
    input_guess(str(a))
        
    
                 
            
def r_num():
    input_guess(str(random.randrange(0,game_range)))
# create frame
f = simplegui.create_frame("Guess the number",150,400)
f.add_button('[0,100)', range100,100)
f.add_button('[0,1000)', range1000,100)
f.add_button('Random number',r_num,100)
f.add_button('Automatic solve',auto,100)
f.add_input("[0,x) custom range",rangeX, 100)
f.add_input("Enter",input_guess, 100)
f.start()
# register event handlers for control elements and start frame


# call new_game 
new_game()


# always remember to check your completed program against the grading rubric