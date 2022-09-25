########## Things to do ##########
# 1. Create Gui...................... Done
# 2. Create Logging system........... Done
# 4. Implement actual system......... WIP
# 5. Implement threading.............

# Ideas
# Download wordlist as a PDF
# Have program read the  PDF
# manipulate the mouse and keyboard
# 
# Edit: PDF system doesnt work as expected, use txt file instead

# as soon as starting, set screen to full using f11 in browser
# base all cords on this.

warn_tag = "[\u001b[31mWARN\u001b[0m] "
info_tag = "[\u001b[36mINFO\u001b[0m] "
okay_tag = "[\u001b[32mOKAY\u001b[0m] "

import datetime


def check_file_existence(File_name):
    # checks if file exists to not cause errors
    file_exists = False
    try:
        file = open(File_name, "x")  # x creates file, returns error if already exists
    except FileExistsError:
        file_exists = True
    except FileNotFoundError:
        file_exists = False
    return file_exists


def Log(tag, text):
    log_tag = ""
    if type(text) == bytes:
        text = text.decode("UTF-8")
    print(tag, text)
    if check_file_existence("log.txt") == False:
        print(warn_tag, "log.txt missing, creating new file")
        log = open("log.txt", "w")
        log.write("[OKAY] Log file created")
        log.close()
    log = open("log.txt", "a")
    if tag == "[\u001b[31mWARN\u001b[0m] ":
        log_tag = "[WARN]"
    elif tag == "[\u001b[36mINFO\u001b[0m] ":
        log_tag = "[INFO]"
    elif tag == "[\u001b[32mOKAY\u001b[0m] ":
        log_tag = "[OKAY]"
    if len(log_tag) < 1:
        log.write(text + "\n")
    else:
        log.write("[" + str(datetime.datetime.now()) + "] " + log_tag + " " + text + "\n")
        
try:
    import ctypes
    import os
    import platform
    import tkinter.messagebox
    from tkinter import *
    from tkinter import ttk

    import urllib.error

    from urllib import request
    import zipfile

    import pynput.keyboard
    from pynput import *
    from PIL import ImageTk, Image, ImageGrab
    import threading
    import time
    from win32api import GetSystemMetrics
    import win32gui

    import key_mouse_logic  # user made
    import read_file  # user made
except ImportError as error:
    Log(warn_tag, "Error 424 libraries missing, please ask creator for a fix\n" + str(error))
    Log(warn_tag, str(error))
    exit()

message = """This program is designed to autocomplete education perfect tasks. 
    This is accomplished by messing with the random question generator system within the site itself. 
    What you need to know, is that you must create a text file in the same directory as this program, 
    name it whatever you want. In this text file, copy + paste the answers and questions from the module you
    wish to autocomplete. You MUST put two spaces between the answers and questions. 
    Once this is done, click the start button, and you'll have 5 seconds to switch to your web browser of choice. 
    Education Perfect must be the current tab open, and should be on the page where the start button exists. 
    The program will then take control of your mouse and keyboard, upon which it will click the start button. 
    To stop the program, press esc.\n\n
    This program is made for purely educational purposes that demonstrate how certain ways randomness can be predicted. 
    Please don't use this program for any cheating, or 'autocompletion', this was made as an experiment.\nNOT FOR CHEATING."""

Log(okay_tag, "Libraries imported")

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    Log(info_tag, "Process started as admin: " + str(is_admin))

system = platform.system()
cwd = os.getcwd()

Log(info_tag, "System detected: " + system)
scr_width = GetSystemMetrics(0)
scr_height = GetSystemMetrics(1)
resolution = (scr_width, scr_height)
Log(info_tag, "Resolution of screen: " + str(scr_width) + "x" + str(scr_height))

def raise_error(priority, Message, err_title=""):
    if priority == 1:
        Log(warn_tag, Message)
        tkinter.messagebox.showerror(title=err_title, message=Message)
    elif priority == 2:
        Log(warn_tag, Message)


def check_file_contents(File_name, mode="r"):
    # Function checks if there is stuff within the file, and isnt just empty
    # Returns a bool on wether file contents are sufficient
    if mode == "rb":
        return True  # TODO: Add functioning file contents checker for binary files

    char_counter = 0  # counts characters
    file = open(File_name, mode)  # reads file data

    Log(info_tag, "Dumping file contents of " + File_name)
    Log("", "-" * 20 + "START" + "-" * 20)

    file = file.readlines()  # Extract contents into an array
    for x in file:  # for each line in file, if line has more than one character
        Log("", x)
        char_counter += len(x.replace("\n", ""))  # adds char count of each line(minus new lines)

    Log("", "-" * 20 + " END " + "-" * 20)
    if char_counter > 10 or len(file) > 4:  # arbitrary values chosen, no meaning behind
        return True  # Contents are alright
    else:
        return False  # Contents are not sufficient


def info_window(Message=message):
    tkinter.messagebox.showinfo(title="Info", message=Message)


def pre_start_checks():
    directories = os.listdir()  # look for relevant files
    instances = 0
    filename = ""
    for file in directories:
        if file[-4::] == ".txt":
            if file != "log.txt":
                instances += 1
                file_exists = True
                filename = file
    if instances > 1:  # if more than one "answer sheet"
        raise_error(1,
                    "There are more than one .txt files in the current folder\nPlease provide only one txt with the correct answers",
                    err_title="413 Payload too large")
        exit_command()
    if instances < 1:
        raise_error(1,
                    "There is no .txt file listed in the same directory. Please provide a txt file in the same directory as this program",
                    err_title="404 File not found")

    if file_exists == True:
        file_contents_check = check_file_contents(filename, "rb")
        if file_contents_check == True:
            Log(okay_tag, "Passed pre-start checks without errors")
            Log(okay_tag, "Delaying for 5 seconds")
            if check_button_state.get() == True:
                Log(info_tag, "Autotab enabled, switching...")
                root.iconify()
                key_mouse_logic.tab()
            else:
                pass
        else:
            Log(warn_tag, "Contents of file seem invalid(under 10 characters, or less than 4 lines)")
            warning_message = "Contents of file not valid.\nPlease be sure to put the answers on new lines, as well as having enough answers."
            tkinter.messagebox.showerror(title="Not enough answers", message=warning_message)
    else:
        Log(warn_tag, "Could not find file located at \"" + filename + "\"")

    key_mouse_logic.start()  # checks if browser is set right
    # also sets up the screen using f11 to full screen the browser
    Log(info_tag, filename + " is used for answers")
    start(filename, resolution)


def start(filename, resolution, ):
    answers = read_file.extract_text(filename)
    if type(answers) == str:  # if returned as string then an error has occured
        raise_error(1,
                    err_title="Answer file open",
                    Message="Could not open " + filename + " due to " + answers
                    )
    Log(info_tag, "Answers sheet dump\n" + str(answers))
    answers = read_file.format_text(answers)
    activity_lessons = [reading_state.get(), listening_state.get(), diction_state.get(), writing_state.get()]
    time.sleep(1)  # lets browser react to changing to f11 mode
    for x in range(0, len(activity_lessons)):
        if activity_lessons[x] == 1:
            lesson = None
            if x == 0:
                lesson = "reading"
            elif x == 1:
                lesson = "listening"
            elif x == 2:
                lesson = "dictation"
            elif x == 3:
                lesson = "writing"
            Log(info_tag, "Changing to lesson " + str(x) + ", " + lesson)
            key_mouse_logic.change_learning_mode(x)
            key_mouse_logic.enter_lesson()
            for y in answers:
                for z in range(0, 2): # type answer 3 times
                    print(y)
                    key_mouse_logic.enter_lesson()
                    key_mouse_logic.do_lesson(y, x)
                    key_mouse_logic.exit_lesson()

            # mode 0 reading
            # mode 1 listening
            # mode 2 dictation
            # mode 3 writing


def exit_command():  # kills threads and processes
    Log(okay_tag, "Killing processes")
    root.destroy()
    exit()


# ------------------- Setup and window stuff-------------------- #
Log(info_tag, "Creating Window[200x300]")
root = Tk()
root.title("Education Perfect Automator")
root.geometry("200x300")

check_button_state = BooleanVar()

reading_state = IntVar(value=1)
writing_state = IntVar(value=1)
listening_state = IntVar(value=1)
diction_state = IntVar(value=1)

frm = ttk.Frame(root, padding=10)

Button(root, text="Start ", command=pre_start_checks).place(x=70, y=40)
Button(root, text=" Info ", command=info_window).place(x=70, y=80)

check_button = Checkbutton(root, text="Auto <Alt> + <Tab> on start", variable=check_button_state, onvalue=True, offvalue=False).place(x=15, y=220)

Reading = Checkbutton(root, text="Reading Activity", variable=reading_state, onvalue=1, offvalue=0).place(x=15, y=140)
Listening = Checkbutton(root, text="Listening Activity", variable=listening_state, onvalue=1, offvalue=0).place(x=15,
                                                                                                                y=160)
Diction = Checkbutton(root, text="Dictaion Activity", variable=diction_state, onvalue=1, offvalue=0).place(x=15, y=180)
Writing = Checkbutton(root, text="Writing Activity", variable=writing_state, onvalue=1, offvalue=0).place(x=15, y=200)

root.mainloop()
