from data import gui;
import os;
import sys;

args = sys.argv;
args.pop(0);

f = True;
try:
	args[0];
except IndexError:
	f = False;
if f:
	if args[0] == "-mod":
		mod = args[1];
	else:
		mod = "main";
else:
	mod = "main";

gui1 = gui.GUI();
gui1.system_start(mod);