import pynput
from pynput.keyboard import Key
from pynput.mouse import Button
import time
import pyperclip

time_delay = 1.5 # time it takes to exit(this is for internet variability)
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()



def start():
    time.sleep(5)
    keyboard.press(Key.f11)
    keyboard.release(Key.f11)
    return (1)

def get_mouse_pos():
    # Read pointer position
    print('The current pointer position is {0}'.format(mouse.position))

def tab():
    keyboard.press(Key.alt)
    keyboard.press(Key.tab)
    time.sleep(0.05)
    keyboard.release(Key.alt)
    keyboard.release(Key.tab)



def enter_lesson(window_scale=1):
    mouse.position = start_button
    time.sleep(0.3)
    mouse.press(Button.left)
    mouse.release(Button.left)
    # Presses the enter button

def do_lesson(answer, lesson_type):
    mouse.position = text_input
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(2)
    # if lesson is writing....
    if lesson_type == 0: # type in english
        print("lesson 0")
        keyboard.type(answer[1])
        print(answer[1])
    if lesson_type == 1: # type in english
        print("lesson 1")
        keyboard.type(answer[1])
        print(answer[1])
    if lesson_type == 2: # type in french
        print("lesson 2")
        keyboard.type(answer[0])
        print(answer[0])
    if lesson_type == 3:
        # type in french
        keyboard.type(answer[0])
        print(answer[0])

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(1)

def exit_lesson():
    mouse.position = exit_button
    mouse.press(Button.left)
    mouse.release(Button.left)
    time.sleep(1)
    mouse.position = exit_button2
    mouse.press(Button.left)
    mouse.release(Button.left)
def change_learning_mode(mode, window_scale=1):
    mode_location = [560, (340 + (50 * mode))]
    # 560 for x
    # 380 + (50 * the mode) for y
    # mode 0 reading
    # mode 1 listening
    # mode 2 dictation
    # mode 3 writing

    mouse.position = (mode_location[0], mode_location[1])
    time.sleep(0.3)
    mouse.press(Button.left)
    mouse.release(Button.left)


    # changes learning mode


# all settings measured in 1920x1080 node
top_of_page      = (0, 70)
bottom_of_page   = (0, 1040)


# -40 on all these
reading_lesson   = (560, 380)
listening_lesson = (560, 430)
dictation_lesson = (560, 480)
writing_lesson   = (560, 530)

start_button     = (560, 1020)

exit_button2     = (542, 975)
exit_button      = (70, 25)

text_input       = (900, 1050)

# top of page is 0, 70
# bottom of page is 1040
#
# Reading   mode lesson located at 560, (380) type in english
# listening mode lesson located at 560, (430) type in english
# Dictation mode lesson located at 560, (480) type in french
# Writing   mode lesson located at 560, (530) type in french
#
# start button located at 560, 1020
# exit  button located at 70, 25
#
# Text form located at 900, 1050

#
# time.sleep(2)
# start()
# time.sleep(1)
# get_mouse_pos()
# for x in range(0, 4):
#     change_learning_mode(x)
