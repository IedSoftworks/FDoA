from tkinter import *
from data import functions;
from data import factions;
from data import gui_content;

def init(gui):
	gui.hook.onStartGame.register(startGame);
	gui.hook.onScreenReload.register(overlay);
	gui.hook.onItemAdd.register(item_add);
	gui.hook.onItemRemove.register(item_remove);
	gui.hook.onFactionValue.register(faction_value);
	gui.texts = [];

def overlay(*back, **gui):
	if hasattr(gui["gui"], "last_event"):
		#Label(back[0], bg="White", width=functions.pro_size(1,0), height=functions.pro_size(1,1)).place(y=functions.pro_size(1,1), x=functions.pro_size(80,0), anchor=N)
		i=0;
		for text in gui["gui"].texts:
			i+=1;
			i2=(i-1)*2.5+1;
			if not i > 5:
				Label(back[0], bg="Gold2", text=text[0], font=gui_content.ch_fontsize("15"), fg=text[1]).place(y=functions.pro_size(i2,1),x=functions.pro_size(80,0), anchor=NW);
def item_add(*args, **keyargs):
	functions.addmsg(keyargs["gui"], "+ "+args[0]+" ("+str(args[1])+")", "green");
def item_remove(*args, **keyargs):
	functions.addmsg(keyargs["gui"], "- "+args[0]+" ("+str(args[1])+")", "red");
def faction_value(*args, **keyargs):
	if args[2] > 0:
		functions.addmsg(keyargs["gui"], "/\ "+args[0]["name"]+" ("+str(args[2])+"%)", "green");
	else:
		functions.addmsg(keyargs["gui"], "\/ "+args[0]["name"]+" ("+str(args[2]*-1)+"%)", "red");
def startGame(*args, **keyargs):
	factions.register({"name":"KNA","value2":97,"value":10});