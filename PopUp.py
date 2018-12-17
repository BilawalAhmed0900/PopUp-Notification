#!/usr/bin/python3
from __future__ import print_function, division

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import multiprocessing as mp
import sys
from time import sleep


def get_dimension_using_Tk(root, default_placing_manager,
                           string, font, font_size):
    longest_line_label =\
        tk.Label(root, text=string, bg="black", fg="grey",
                 font=(font, font_size))
    # longest_line_label.configure(anchor="center")
    try:
        getattr(longest_line_label, default_placing_manager)()
    except AttributeError:
        print("Only (pack|grid|place) are allowed as default_placing_manager")
        return -1, -1

    longest_line_label.update_idletasks()

    width = longest_line_label.winfo_width()
    height = longest_line_label.winfo_height()
    longest_line_label.destroy()

    return width, height


def show_messagebox(title, message):
    FONT_SIZE = 16
    PAD_X = 20
    PAD_Y = 10

    main_window = tk.Tk()
    main_window.overrideredirect(1)

    main_window.call("wm", "attributes", ".", "-topmost", "true")
    main_window.attributes('-alpha', 0.8)
    main_window.config(bg="black")

    main_frame = tk.Frame(main_window)
    main_frame.configure(bg="black")
    main_frame.pack()

    all_lines = []

    all_lines.extend(title.split("\n"))
    all_lines.append("\n")
    all_lines.extend(message.split("\n"))

    number_of_lines = len(all_lines)
    longest_line = ""

    for _, line in enumerate(all_lines):
        if len(line) > len(longest_line):
            longest_line = line

    longest_line_width, _ = get_dimension_using_Tk(main_frame, "grid",
                                                   longest_line,
                                                   "Times New Roman",
                                                   FONT_SIZE)

    longest_line_width += 2 * PAD_X

    line_height = FONT_SIZE * 1.50
    all_lines_height = int(number_of_lines * line_height)
    all_lines_height += 2 * PAD_Y

    least_width = 400
    least_height = 65

    least_width = least_width\
        if longest_line_width < least_width else longest_line_width

    least_height = least_height\
        if all_lines_height < least_height else all_lines_height

    # Smooth entry
    width = 0
    while width < least_width:
        main_window.geometry("{}x{}-0-40".format(width, least_height))

        main_window.update()
        main_window.update_idletasks()
        width += 20

    title_label =\
        tk.Label(main_frame, text=title, bg="black", fg="silver",
                 font=("Times New Roman", FONT_SIZE))
    # title_label.configure(anchor="w")
    title_label.grid(row=0, column=0, padx=PAD_X-5, pady=PAD_Y+5, sticky="W")
    # title_label.pack(padx=20)

    message_label =\
        tk.Label(main_frame, text=message, bg="black", fg="grey",
                 font=("Times New Roman", FONT_SIZE))
    message_label.configure(anchor="center")
    message_label.grid(row=2, column=0, padx=PAD_X, pady=PAD_Y)
    # message_label.pack()

    main_window.mainloop()


def show_notification(title, message, SECONDS=3):
    box_process = mp.Process(target=show_messagebox, args=(title, message))
    box_process.start()
    sleep(SECONDS)
    box_process.terminate()


if getattr(sys, 'frozen', False):
    mp.freeze_support()
