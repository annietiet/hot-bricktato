import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk


HEIGHT = 500
WIDTH = 700
BG_COLOR = "#505591"
TEXT_COLOR = "#dde0eb"
NUM_PLAYERS = 0
NUM_PLAYERS_STR = "NUMBER OF PLAYERS: " + str(NUM_PLAYERS)


root = tk.Tk()
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg=BG_COLOR)
frame.place(relwidth= 1, relheight=1)

title = tk.Label(frame, text="LET'S PLAY HOT BRICKTATO", bg=BG_COLOR, fg=TEXT_COLOR, pady= 30, font=("Helvetica 30 bold"))
title.pack()

load1 = Image.open("images/rickyt.png")
render1 = ImageTk.PhotoImage(load1)

bricky = tk.Label(frame, image=render1, bg=BG_COLOR)
bricky.image = render1
bricky.place(relx= .5, rely= .5, anchor="center")


players_label = tk.Label(frame, text=NUM_PLAYERS_STR, pady="30", bg=BG_COLOR, fg=TEXT_COLOR, font=("Helvetica 15"))
players_label.place(relx= .5, rely= 1, anchor="s")
root.mainloop()