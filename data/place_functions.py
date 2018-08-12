import random;
import os;
import math;
from data import functions;
from tkinter import *;
from tkinter import font;
from functools import partial
from data import gui_content;

def register(data):
	placejson = get_places();
	place = {};
	
	# --#										#
	place["options"]=data["options"];			#
		# Optionen:
		# 	- events:
		#		- enterf: Event, das beim ersten Betreten ausgeführt wird.
		#		- entern: Event, das bei jedem weiteren Betreten ausgeführt wird.
		#		- random: Array von Events, die beim Aufenthalt in diesem Ort zufällig auftreten können.
		#			stil: [["Ordner","Event"],["Ordner","Event"]]
		#		- clickable: Array von Events, die beim Aufenthalt in diesem Ort per Knopfdruck ausgelöst werden können.
		#			stil: [["Ordner","Event","Knopftext"],["Ordner","Event","Knopftext"]]
		#	- garage: 
		#		- storage: Array von Fahrzeugen, die sich von Anfang an in der Garage dieses Ortes befinden sollen.
		#		- size:	Anzahl der Stellplätze in dieser Garage.
		#		- disable: Auf True setzen wenn dieser Ort keine Garage anbieten soll.
		#	- storage:
		#		- storage: Array von Items, die sich von Anfang an in dem Lagerplatz dieses Ortes befinden sollen.
		#		- size: Anzahl der Items, die dieser Lagerplatz fassen können soll.
		#		- disable: Auf True setzen, wenn dieser Ort keinen Lagerplatz anbieten soll.
	# --#										#
	print(data);
	check = True;								#
	try:										#
		exec("print("+str(data["garage"])+")");		#
	except:										#
		check = False;							#
	if not check:									#
		place["garage"] = {"storage":{},"size":1,"disable":False};	#
	else:											#
		place["garage"] = data["garage"];		#
	if place["garage"]["disable"]:
		place["garage"]["size"]=1;
	# --#										#
	check = True;								#
	try:										#
		exec("print("+str(data["storage"])+")");		#
	except:										#
		check = False;							#
	if not check:									#	
		place["storage"] = {"storage":{},"size":16,"disable":False};#
	else:											#
		place["storage"] = data["storage"];		#
	# --#										#
	place["system"] = {"first":True};
	placejson[data["name"]] = place;
	save_places(placejson);
def enterplace(gui, name):
	gd = functions.get_gamedata();
	place = get_place(name);
	gd["place"] = name;
	if place["system"]["first"]:
		gd["places"][name]["system"]["first"] = False;
		functions.save_gamedata(gd);
		if place["options"]["events"]["enterf"][0] != "None":
			gui.game(place["options"]["events"]["enterf"][1], place["options"]["events"]["enterf"][0], ["enterf", name]);
		else:
			hub(gui);
	else:
		functions.save_gamedata(gd);
		if place["options"]["events"]["entern"][0] != "None":
			gui.game(place["options"]["events"]["entern"][1], place["options"]["events"]["entern"][0], ["entern", name]);
		else:
			hub(gui);
def hub(gui):
	gui.clear_screen();
	back = gui.hintergrund();
	back.pack();
	gd = functions.get_gamedata();
	place = get_place(gd["place"]);
	
	Text = Canvas(back, bg="Gold2", highlightthickness=0);
	Text.place(x=functions.pro_size(10,0), y=functions.pro_size(10,1));
	Label(Text, text="Willkommen in "+gd["place"], font=gui_content.ch_fontsize(32), bg="Gold2").grid(row=1,columnspan=3,sticky=W);
	Button(Text, text="Garage", command=partial(garage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,padx=5,pady=5);
	if not place["storage"]["disable"]:
		Button(Text, text="Lager", command=partial(storage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,column=1,padx=5,pady=5);
	else:
		Button(Text, text="Lager", state=DISABLED, command=partial(storage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,column=1,padx=5,pady=5);
	if len(place["options"]["events"]["clickable"]) > 0:
		Label(Text, text="Aktionen:", font=gui_content.ch_fontsize(20), bg="Gold2").grid(row=3,sticky=W,columnspan=3);
		Scroll = Canvas(Text, bg="Gold2", highlightthickness=0, width=functions.pro_size(80,0), height=functions.pro_size(10,1));
		Scroll.grid(row=4,sticky=W,columnspan=200);
		Scroll1 = functions.VerticalScrolledFrame(Scroll);
		Scroll1.place(x=0,y=0,width=functions.pro_size(100,0));
		key = 0;
		for value in place["options"]["events"]["clickable"]:
			row = math.floor(key / 6);
			column = key % 6;
			key+=1;
			Button(Scroll1.interior, text=value[2], command=partial(clickable, gui, value), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=row,column=column,padx=5,pady=5);
			
def garage(gui):
	print("");
def storage(gui):
	print("");
def clickable(gui, event):
	gui.game(event[1], event[0]);
def get_places():
	try:
		return functions.get_gamedata()["places"];
	except:
		return {};
def get_place(name):
	return get_places()[name];
def save_places(array):
	var = functions.get_gamedata();
	var["places"] = array;
	functions.save_gamedata(var);