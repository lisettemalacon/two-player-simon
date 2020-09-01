import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import time
import pygame, sys
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

# input set ups
input_pin1 = 12
input_pin2 = 16
input_pin3 = 20
input_pin4 = 21
stop_input = 24
check_input = 26

led1 = 4
led2 = 17
led3 = 27
led4 = 6

GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)

GPIO.output(led1,0)
GPIO.output(led2,0)
GPIO.output(led3,0)
GPIO.output(led4,0)

GPIO.setup(input_pin1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(input_pin2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(input_pin3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(input_pin4,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(stop_input,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(check_input,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pygame.mixer.init()

beep1 = pygame.mixer.Sound('/home/pi/Music/note1.wav')
beep2 = pygame.mixer.Sound('/home/pi/Music/note2.wav')
beep3 = pygame.mixer.Sound('/home/pi/Music/note3.wav')
victory = pygame.mixer.Sound('/home/pi/Music/vic.wav')
lose = pygame.mixer.Sound('/home/pi/Music/lose.wav')
start = pygame.mixer.Sound('/home/pi/Music/start.wav')
copy = pygame.mixer.Sound('/home/pi/Music/copy.wav')    

## starting program
time_pause = 0.5
first_press = False
stop_already = False
second_press = False

# starts game and timer with the first button push // also catches second push so it knows when the first player finishes
def start_game(input):
    global first_press
    global stop_already
    global second_press
    
    if input == 1:
        if first_press == False and stop_already == False:
            first_press = True
            stop_already = True
            start.play()
            print('first press')
           
        elif first_press == False and stop_already == True:
            print('second press')
            first_press = True
            stop_already = False
            second_press = True
            copy.play()
     
    else:
        if first_press == True and stop_already == True:
            first_press = False
    
        elif first_press == True and stop_already == False:
            first_press = False
    time.sleep(0.05)
       
# second player gets the breadboard and needs to match the first pattern
pattern_match = False
reset_game = False
def check_pattern(input):
    global pattern_match
    global reset_game
    
    if input == 1:
        
        if len(button_pattern) != len(button_pattern2):
            pattern_match = False
            print('better luck next time!')
            end_game()
            reset_game = True
        else:
            
            for i in range(0,len(button_pattern)):
                if button_pattern2[i] != button_pattern[i]:
                    pattern_match = False
                else:
                    pattern_match = True
            if pattern_match == False:
                print('better luck next time!')
                end_game()
                reset_game = True
            else:
                print('nice match!')
                end_game()
                reset_game = True
            
def end_game():
    if pattern_match == True:
        victory.play()
        GPIO.output(led4,1)
        time.sleep(time_pause)
        GPIO.output(led4,0)        
        time.sleep(time_pause)
        GPIO.output(led4,1)
        time.sleep(time_pause)
        GPIO.output(led4,0)
        
    if pattern_match == False:
        lose.play()
        GPIO.output(led1,1)
        GPIO.output(led2,1)
        GPIO.output(led3,1)
        time.sleep(2)
        GPIO.output(led1,0)
        GPIO.output(led2,0)
        GPIO.output(led3,0)
       
#functions to check button inputs       
pushed1 = False
add_to_list1 = False
def input_check1(input):
    global pushed1
    global add_to_list1
    
    if first_on == 1 and pushed1 == False:
        GPIO.output(led1,1)
        beep1.play()
        time.sleep(time_pause)        
        pushed1 = True
        add_to_list1 = True
        print('pushed 1')
        
    elif first_on == 0 and pushed1 == True:
        GPIO.output(led1,0)
        pushed1 = False
        add_to_list1 = False
        print('released 1')
              
pushed2 = False
add_to_list2 = False
def input_check2(input):
    global pushed2
    global add_to_list2
    
    if second_on == 1 and pushed2 == False:
        GPIO.output(led2,1)
        beep2.play()
        time.sleep(time_pause)
        print('pushed 2')
        add_to_list2 = True
        pushed2 = True
        
    if second_on == 0 and pushed2 == True:
        GPIO.output(led2,0)
        pushed2 = False
        add_to_list2 = False
        print('released 2')

pushed3 = False
add_to_list3 = False
def input_check3(input):
    global pushed3
    global add_to_list3
    
    if third_on == 1 and pushed3 == False:
        GPIO.output(led3,1)
        beep3.play()
        time.sleep(time_pause)
        pushed3 = True
        add_to_list3 = True
        print('pushed 3')
    if third_on == 0 and pushed3 == True:
        GPIO.output(led3,0)
        pushed3 = False
        add_to_list3 = False
        print('released 3')

# adds the first player's pattern into a list
button_pattern = []
already_added1 = False
already_added2 = False
already_added3 = False
already_added4 = False
def collect_pattern1():
    global already_added1
    global already_added2
    global already_added3
    global already_added4
    
    if add_to_list1 == True and already_added1 == False:
        already_added1 = True
        button_pattern.append('one')
        print(button_pattern)
    if add_to_list1 == False:
        already_added1 = False

    if add_to_list2 == True and already_added2 == False:
        already_added2 = True
        button_pattern.append('two')
        print(button_pattern)
    if add_to_list2 == False:
        already_added2 = False

    if add_to_list3 == True and already_added3 == False:
        already_added3 = True
        button_pattern.append('three')
        print(button_pattern)
    if add_to_list3 == False:
        already_added3 = False
        
# add the second player's pattern into a list (trying to match the first player)         
button_pattern2 = []   
def collect_pattern2():
    global already_added1
    global already_added2
    global already_added3
    global already_added4
    
    if add_to_list1 == True and already_added1 == False:
        already_added1 = True
        button_pattern2.append('one')
        print(button_pattern2)
    if add_to_list1 == False:
        already_added1 = False

    if add_to_list2 == True and already_added2 == False:
        already_added2 = True
        button_pattern2.append('two')
        print(button_pattern2)
    if add_to_list2 == False:
        already_added2 = False

    if add_to_list3 == True and already_added3 == False:
        already_added3 = True
        button_pattern2.append('three')
        print(button_pattern2)
    if add_to_list3 == False:
        already_added3 = False
        
message_box = False      
def message():
    global message_box
    if message_box == False:
        messagebox.showinfo("Instructions","Welcome to two-player matching! The goal of the game is to match the first player's pattern. Press the black button to start. Use the three blue buttons to make a pattern. Press the black button again when you're ready for player 2 to repeat the pattern. Player 2 presses the red button to submit the pattern to check once done. Press the black button to play again! Click OK to start playing.")
        message_box = True    

while True:
    first_on = GPIO.input(input_pin1)
    second_on = GPIO.input(input_pin2)
    third_on = GPIO.input(input_pin3)
    fourth_on = GPIO.input(input_pin4)
    stop_button = GPIO.input(stop_input)
    check_button = GPIO.input(check_input)
    message()
       
    start_game(stop_button)
    
    if first_press == False and stop_already == True and second_press == False:
        collect_pattern1()
        input_check1(first_on)
        input_check2(second_on)
        input_check3(third_on)
        
    if second_press == True:
            collect_pattern2()
            input_check1(first_on)
            input_check2(second_on)
            input_check3(third_on)
                        
    check_pattern(check_button)
    
    # clears lists after a match
    if reset_game == True:
        button_pattern = []
        button_pattern2 = []
        second_press = False
        print(button_pattern)
        print(button_pattern2)
        reset_game = False
