import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk


HEIGHT = 500
WIDTH = 700
BG_COLOR = "#505591"


root = tk.Tk()
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg=BG_COLOR)
frame.place(relwidth= 1, relheight=1)

title = tk.Label(frame, text="HOT BRICKTATO", bg=BG_COLOR, pady= 10, font=('Arial', 50))
title.pack()

image1 = Image.open("images/rickyt.png")
image1TK = Image.TK.PhotoImage(image1)

bricky = tkinter.Label(image=image1TK)
bricky.image = image1TK

bricky.place(relx = .5, rely = .5)



root.mainloop()