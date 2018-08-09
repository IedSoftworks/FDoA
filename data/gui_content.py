from tkinter import *;

def button(content1, text, x, y, command, font=(('MS', 'Sans', 'Serif'), 8), color=["green", "black"], bigest="x"):
	if bigest != "x":
		Button(content1, text=text, command=command, font=font, bg=color[0], bd=8, fg=color[1]).place(x=x, y=y, width=bigest[0], height=bigest[1]);
	else:
		Button(content1, text=text, command=command, font=font, bg=color[0], bd=8, fg=color[1]).place(x=x, y=y);

def ch_fontsize(wishedsize):
	return (('MS', 'Sans', 'Serif'), wishedsize)
