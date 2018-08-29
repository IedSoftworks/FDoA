import random;
import os;
import collections;
from data import functions;
from data import gui_content
from data import event_functions;
from data import place_functions;
from tkinter import *;
from tkinter import font;
import math;
from functools import partial
import hashlib

def register(data):
	gd = get_cons();
	id = random.random() * 1000000;
	id = hashlib.md5(str(id).encode('utf-8')).hexdigest();
	try:
		exec("print(\""+data["name"]+"\")");
	except:
		data["name"]="Container";
	try:
		exec("print(\""+str(data["size"])+"\")");
	except KeyError:
		data["size"]=1000000000;
	try:
		exec("print(\""+str(data["removeonexit"])+"\")");
	except:
		data["removeonexit"]=False;
	gd[id]=data;
	functions.add_json_string("user\gamedata.json", "containers", gd);
	from data.getgui import gui;
	gui.hook.onContainerRegister.fire(id);
	return id;
def open(event, id, func, gui):
	gui.clear_screen();
	hintergrund = gui.hintergrund();
	hintergrund.pack();
	cons = get_cons();
#	print(cons);
	container = cons[id];
	gui.hook.onContainerOpen.fire(id, container);

	Label(hintergrund, text=container["name"], font=gui_content.ch_fontsize("24"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);		
	Button(hintergrund, text="Zurück", command=partial(exit, event, id, func, gui), font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(5,1), x=functions.pro_size(50,0), anchor=N);
	Button(hintergrund, text="Container", command=partial(open, event, id, func, gui), bg="red", font=gui_content.ch_fontsize("16")). place(y=functions.pro_size(5,1), x=functions.pro_size(45,0), anchor=N);
	Button(hintergrund, text="Inventar",  command=partial(inve, event, id, func, gui),           font=gui_content.ch_fontsize("16")). place(y=functions.pro_size(5,1), x=functions.pro_size(55,0), anchor=N);
	
	inventar1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
	inventar1.place(anchor=N, x=functions.pro_size(50,0), y=functions.pro_size(10,1));
	inventar = functions.VerticalScrolledFrame(inventar1);
	inventar.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));
	
	inventar_content = container["inv"];
	if len(inventar_content.items()) == 0:
		Label(inventar.interior, text="Keine Items", fg="black", font=gui_content.ch_fontsize("32")).place(x=functions.pro_size(50,0), y=functions.pro_size(50,1), anchor=CENTER);
	else:
	
		xrow = 0;
		for inv, value in inventar_content.items():
			xrow +=1
			newcanvas = {};
			newcanvas[xrow] = Canvas(inventar.interior, bg="green", width=functions.pro_size(90,0), height=functions.pro_size(9,1));
			newcanvas[xrow].grid(row=xrow);
			Label(newcanvas[xrow], text=inv, font=gui_content.ch_fontsize("40"), bg="green", fg="white").place(x=functions.pro_size(1,0), y=functions.pro_size(4.5,1), anchor=W);
			Label(newcanvas[xrow], text="Anzahl: "+str(value), fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);
			if value > 0:
				Button(newcanvas[xrow], text="1",   fg="white",bg="green",command=partial(move, event, id, func, -1, inv, 1, gui)  ).place(y=functions.pro_size(9,1), x=functions.pro_size(84,0), anchor=SE);
			if value > 9:
				Button(newcanvas[xrow], text="10",  fg="white",bg="green",command=partial(move, event, id, func, -1, inv, 10, gui) ).place(y=functions.pro_size(9,1), x=functions.pro_size(83,0), anchor=SE);
			if value > 99:
				Button(newcanvas[xrow], text="100", fg="white",bg="green",command=partial(move, event, id, func, -1, inv, 100, gui)).place(y=functions.pro_size(9,1), x=functions.pro_size(82,0), anchor=SE);
			Button(newcanvas[xrow], text="A", fg="white",bg="green",command=partial(move, event, id, func, -1, inv, value, gui)).place(y=functions.pro_size(9,1), x=functions.pro_size(85,0), anchor=SE);
			Label(newcanvas[xrow], text="Übertragen:", fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(80,0), anchor=SE);
def inve(event, id, func, gui):	
	gui.clear_screen();
	hintergrund = gui.hintergrund();
	hintergrund.pack();
	cons = get_cons();
	container = cons[id];

	Label(hintergrund, text=container["name"], font=gui_content.ch_fontsize("24"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);		
	Button(hintergrund, text="Zurück", command=partial(exit, event, id, func, gui), font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(5,1), x=functions.pro_size(50,0), anchor=N);
	Button(hintergrund, text="Container", command=partial(open, event, id, func, gui),           font=gui_content.ch_fontsize("16")). place(y=functions.pro_size(5,1), x=functions.pro_size(45,0), anchor=N);
	Button(hintergrund, text="Inventar",  command=partial(inve, event, id, func, gui), bg="red", font=gui_content.ch_fontsize("16")). place(y=functions.pro_size(5,1), x=functions.pro_size(55,0), anchor=N);
	
	inventar1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
	inventar1.place(anchor=N, x=functions.pro_size(50,0), y=functions.pro_size(10,1));
	inventar = functions.VerticalScrolledFrame(inventar1);
	inventar.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));
	
	inventar_content = functions.get_inventory();
	if len(inventar_content.items()) == 0:
		Label(inventar.interior, text="Keine Items", fg="black", font=gui_content.ch_fontsize("32")).place(x=functions.pro_size(50,0), y=functions.pro_size(50,1), anchor=CENTER);
	else:
	
		xrow = 0;
		for inv, value in inventar_content.items():
			xrow +=1
			newcanvas = {};
			newcanvas[xrow] = Canvas(inventar.interior, bg="green", width=functions.pro_size(90,0), height=functions.pro_size(9,1));
			newcanvas[xrow].grid(row=xrow);
			Label(newcanvas[xrow], text=inv, font=gui_content.ch_fontsize("40"), bg="green", fg="white").place(x=functions.pro_size(1,0), y=functions.pro_size(4.5,1), anchor=W);
			Label(newcanvas[xrow], text="Anzahl: "+str(value), fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);
			if value > 0:
				Button(newcanvas[xrow], text="1",   fg="white",bg="green",command=partial(move, event, id, func, 1, inv, 1, gui)  ).place(y=functions.pro_size(9,1), x=functions.pro_size(84,0), anchor=SE);
			if value > 9:
				Button(newcanvas[xrow], text="10",  fg="white",bg="green",command=partial(move, event, id, func, 1, inv, 10, gui) ).place(y=functions.pro_size(9,1), x=functions.pro_size(83,0), anchor=SE);
			if value > 99:
				Button(newcanvas[xrow], text="100", fg="white",bg="green",command=partial(move, event, id, func, 1, inv, 100, gui)).place(y=functions.pro_size(9,1), x=functions.pro_size(82,0), anchor=SE);
			Button(newcanvas[xrow], text="A", fg="white",bg="green",command=partial(move, event, id, func, 1, inv, value, gui)).place(y=functions.pro_size(9,1), x=functions.pro_size(85,0), anchor=SE);
			Label(newcanvas[xrow], text="Übertragen:", fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(80,0), anchor=SE);
def exit(event, id, func, gui):
	cons = get_cons();
	con = cons[id];
	if con["removeonexit"]:
		del cons[id];
		gd = functions.get_gamedata();
		gd["containers"]=cons;
		functions.save_gamedata(gd);
	if not event == "none":
		exec("event."+func+"()");
	else:
		place_functions.hub(gui, False, True);
def get_cons():
	try:
		return functions.get_gamedata()["containers"];
	except:
		return {};
def move(event, id, func, direction, item, amount, gui):
	conf = get_cons()[id];
	con = conf["inv"];
	inv = functions.get_inventory();
	if direction == 1:
		gui.hook.onContainerMoveToCon.fire(id, conf, inv, item, amount, event, func);
	if direction == -1:
		gui.hook.onContainerMoveToInv.fire(id, conf, inv, item, amount, event, func);
	mistake=False;
	if direction == 1:
		if not event_functions.check_item(item) >= amount:
			mistake=True;
	else:
		if not con[item] >= amount:
			mistake=True;
	if not mistake:
		try: 
			exec("print(\""+str(con[item])+"\")")
		except KeyError:
			con[item]=0;
		try: 
			exec("print(\""+str(inv[item])+"\")")
		except KeyError:
			inv[item]=0;
		if direction == 1:
			famount = 0;
			for item, amo in con.items():
				famount += amo;
			if (conf["size"] - famount - amount) < 0:
				amount += (conf["size"] - famount - amount);
		#	print("Checked. famount:"+str(famount));
		con[item]+=amount*direction;
		inv[item]+=amount*direction*-1;
		gd = functions.get_gamedata();
		gd["inventory"]=inv;
		gd["containers"][id]["inv"]=con;
		functions.save_gamedata(gd);
		if direction == 1:
			inve(event, id, func, gui);
		else:
			open(event, id, func, gui);
def openx(event, id, func):
	open(event, id, func, event.gui);
def openxx(id, gui):
	open("none", id, "", gui);