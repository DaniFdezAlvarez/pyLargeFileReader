# coding=utf-8
__author__ = 'Dani'

from Tkinter import *
from tkFileDialog import *


## ROOT

root = Tk()
root.resizable(0, 0)
root.geometry("830x470")


def execute_function(f):
    root.after(200, f)


## BT_FUNCTIONS AND LOGIC

def f_clear(text_widget):
    text_widget.delete("1.0", END)


def f_path(entry_widget):
    file_path = askopenfilename()
    entry_widget.delete(0, END)
    entry_widget.insert(0, file_path)


def is_valid_lines(text):
    try:
        number = int(text)
        if number > 0:
            return True
        return False
    except:
        return False

def is_valid_start_line(text):
    if text in [None, ""]:
        return True
    try:
        number = int(text)
        if number >= 0:
            return True
        return False
    except:
        return False



def is_valid_path(text):
    try:
        with open(text, "r"):
            return True
    except:
        return False


def is_valid_break_char(text):
    if len(text) == 0:
        return True
    if len(text) == 1:
        return True
    elif len(text) == 2 and text[0] == "\\":
        return True
    return False


def error_message(text_widget, message):
    text_widget.delete("1.0", END)
    text_widget.insert("1.0", "ERROR: " + message)


def read_lines_in_chunks(in_stream, break_char):
    previous_result = ""
    while True:
        data = in_stream.read(1024)
        if not data:
            break
        last_index = 0
        for i in range(0, len(data)):
            if data[i] == break_char:
                yield previous_result + data[last_index:i + 1]
                previous_result = ""
                last_index = i + 1
        previous_result += data[last_index:]


def decide_break_char(text):
    if len(text) == 0:
        return "\n"
    elif len(text) == 1:
        return text
    elif text == "\\n":
        return "\n"
    elif text == "\\t":
        return "\t"
    elif text == "\\r":
        return "\r"
    else:
        return "\n"  # This shuold not happen



def f_view(spinbox, entry_path, entry_break_char, text_widget, progress_bar=None):
    text_widget.delete("1.0", END)

    if not is_valid_path(entry_path.get()):
        error_message(text_widget, "The specified path is not valid or points to a not accessible file")
        return
    if not is_valid_lines(spinbox.get()):
        error_message(text_widget, "Invalid number of lines")
        return
    if not is_valid_start_line(spin_start_line.get()):
        error_message(text_widget, "Invalid start line")
        return
    if not is_valid_break_char(entry_break_char.get()):
        error_message(text_widget, "Invalid line separator. Use a single char (you can scape it with '\\')")
        return

    n_lines = int(spinbox.get())
    start_line = int(spin_start_line.get())
    counter = 0
    result = ""
    target_line = n_lines + start_line
    break_char = decide_break_char(entry_break_char.get())
    with open(entry_path.get(), "r") as in_stream:
        for line in read_lines_in_chunks(in_stream, break_char):
            if counter >= target_line:
                break
            if counter >= start_line:
                result += line
            counter += 1

    text_widget.insert(1.0, result)



## TEXT

frame_text = Frame(root)
frame_text.pack(side=BOTTOM, fill=X)


scrollbar_y = Scrollbar(frame_text)
scrollbar_y.pack(side=RIGHT, fill=Y)

scrollbar_x = Scrollbar(frame_text, orient=HORIZONTAL)
scrollbar_x.pack(side=BOTTOM, fill=X)


target_text = Text(frame_text, wrap=NONE, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
target_text.pack(fill=BOTH)

scrollbar_y.config(command=target_text.yview)
scrollbar_x.config(command=target_text.xview)


## PATH

frame_path = Frame(master=root)
string_label_path = StringVar()
string_label_path.set("Path: ")
label_path = Label(frame_path, textvar=string_label_path)
label_path.pack(side=LEFT)

button_path = Button(frame_path, text="File...", command=lambda: execute_function(f_path(entry_path)))

entry_path = Entry(frame_path, width=125)
entry_path.pack(side=LEFT, fill=X)
button_path.pack(side=LEFT)

frame_path.pack(side=TOP, fill=X)


## MAIN CONTROLS

frame_controls = Frame(root)

#Spinner  N LINES
string_label_spin = StringVar()
string_label_spin.set("Number of lines: ")
label_spin = Label(frame_controls, textvar=string_label_spin)
label_spin.pack(side=LEFT)
spinner = Spinbox(frame_controls, from_=0, to=1000000, width=10)
spinner.pack(side=LEFT)

#Spiner Start line
string_label_start = StringVar()
string_label_start.set("Start line (def. 0): ")
label_start = Label(frame_controls, textvar=string_label_start)
label_start.pack(side=LEFT)
spin_start_line = Spinbox(frame_controls, from_=0, to=10000000, width=10)
spin_start_line.pack(side=LEFT)

frame_controls.pack(side=TOP, fill=BOTH)


# bt clear and view

bt_clear = Button(frame_controls, text="Clear", command=lambda: execute_function(f_clear(target_text)))
bt_view = Button(frame_controls, text="View", command=lambda: execute_function(f_view(spinner, entry_path, entry_break, target_text)))

bt_view.pack(side=RIGHT)
bt_clear.pack(side=RIGHT)

# Breaking char
string_label_break = StringVar()
string_label_break.set("   Line separator (default \\n, special chars scaped with \\ are allowed): ")
label_break = Label(frame_controls, textvar=string_label_break)
label_break.pack(side=LEFT)

entry_break = Entry(frame_controls, width=4)
entry_break.pack(side=LEFT)



## EXECUTE

root.mainloop()
