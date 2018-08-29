from tkinter import *;
from data import functions;

def init(gui):
	gui.hook.onScreenReload.register(debug);

def debug(*args, **keywargs):
	Label(args[0], text=str(functions.getStackDepth()),bg="Gold2",fg="green").place(x=0,y=0);