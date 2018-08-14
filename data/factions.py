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

def register(data, override=False):
	factions = get_factions();
	if not "value" in data:
		data["value"]=0;
	cancel=False;
	if data["name"] in factions:
		if not override:
			cancel=True;
	if not cancel:
		factions[data["name"]]=data;
		gd = functions.get_gamedata();
		gd["factions"]=factions;
		functions.save_gamedata(gd);
def get_factions():
	try:
		return functions.get_gamedata()["factions"];
	except:
		return {};
def overview(gui, self):
	self.clear_screen1();
	back = self.hintergrund;
	gd = functions.get_gamedata();
	fac = get_factions();
	Text = Canvas(back, bg="Gold2", highlightthickness=0);
	Text.place(x=functions.pro_size(10,0), y=functions.pro_size(10,1));
	Label(Text, text="Fraktions-Übersicht", font=gui_content.ch_fontsize(32), bg="Gold2").grid(row=0,sticky=W);
	Button(Text, text="Zurück", command=self.hub_menu, font=gui_content.ch_fontsize(26), bg="Gold2").grid(row=1,sticky=W);
	Label(Text, text="Fraktions-Übersicht", font=gui_content.ch_fontsize(32), bg="Gold2", fg="Gold2").grid(row=0,column=1,sticky=W);
	keywords = {-100:["Tötung auf Sicht","red4","white"],-90:["Extrem Aggressiv","red2","white"],-66:["Extrem Misstrauisch","firebrick2","black"],-33:["Misstrauisch","IndianRed1","black"],-3:["Neutral","beige","black"],3:["Akzeptiert","PaleGreen1","black"],33:["Vertraut","green2","black"],66:["Extrem Vertraut","green4","white"],90:["Blind Vertraut","dark green","white"]};
	row = 1
	for name, data in fac.items():
		row += 1
		Label(Text, text=name+":",               font=gui_content.ch_fontsize(24), bg="Gold2",   fg="black"   ).grid(row=row,column=0,sticky=W);
		Label(Text, text=str(data["value"])+"%", font=gui_content.ch_fontsize(24), bg="Gold2",   fg="black"   ).grid(row=row,column=1,sticky=W);
		Label(Text, text="[",                    font=gui_content.ch_fontsize(24), bg="Gold2",   fg="black"   ).grid(row=row,column=2,sticky=W);
		for value, keyw in keywords.items():
			if data["value"] >= value:
				keyword = keyw;
		Label(Text, text="[",                    font=gui_content.ch_fontsize(24), bg="Gold2",   fg="black"   ).grid(row=row,column=2,sticky=W);
		Label(Text, text=keyword[0],             font=gui_content.ch_fontsize(24), bg=keyword[1],fg=keyword[2]).grid(row=row,column=3,sticky=W);
		Label(Text, text="]",                    font=gui_content.ch_fontsize(24), bg="Gold2",   fg="black"   ).grid(row=row,column=4,sticky=W);
def get_value(name):
	try:
		return get_factions()[name]["value"];
	except:
		return 0;
def p(name, value=1):
	value(name, value);
def n(name, value=1):
	value(name, value*-1);
def value(name, value):
	value *= 1.5;
	facs = get_factions();
	fac = facs[name];
	divide = fac["value"] / 10;
	if divide == 0:
		divide = 1;
	value = value / divide;
	fac["value"]+=value;
	gd = functions.get_gamedata();
	facs[name]=fac;
	gd["factions"]=facs;
	functions.save_gamedata(gd);
	