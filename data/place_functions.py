import random;
import os;
import collections;
from data import functions;

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
		#		- clickable: Array von Events, die beim Aufenthalt in diesem Ort per Knopfdruck ausgelöst werden können.
		#	- garage: 
		#		- storage: Array von Fahrzeugen, die sich von Anfang an in der Garage dieses Ortes befinden sollen.
		#		- size:	Anzahl der Stellplätze in dieser Garage.
		#	- storage:
		#		- storage: Array von Items, die sich von Anfang an in dem Lagerplatz dieses Ortes befinden sollen.
		#		- size: Anzahl der Items, die dieser Lagerplatz fassen können soll.
	# --#										#
	check = True;								#
	try:										#
		exec("print("+data["garage"]+")");		#
	except:										#
		check = False;							#
	if not check:									#
		place["garage"] = {"storage":{},"size":1};	#
	else:											#
		place["garage"] = data["garage"];		#
	# --#										#
	check = True;								#
	try:										#
		exec("print("+data["storage"]+")");		#
	except:										#
		check = False;							#
	if not check:									#	
		place["storage"] = {"storage":{},"size":16};#
	else:											#
		place["storage"] = data["storage"];		#
	# --#										#
	
	placejson[data["name"]] = place;
	save_places(placejson);
<<<<<<< HEAD
<<<<<<< HEAD
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
		scrollbar = Scrollbar(Text);
		scrollbar.grid(row=4, column=2, sticky=E);
		c = Canvas();
		c.pack();
		Scroll = Listbox(c, yscrollcommand=scrollbar.set, bg="Gold2", highlightthickness=0, width=functions.pro_size(80,0), height=functions.pro_size(10,1));
		key = 0;
		for value in place["options"]["events"]["clickable"]:
			Scroll.insert(END, "Hi");
		Scroll.pack(side=LEFT, fill=BOTH);
		scrollbar.config(command=Scroll.yview)
			
def garage(gui):
	print("");
def storage(gui):
	print("");
def clickable(gui, event):
	gui.game(event[1], event[0]);
=======
>>>>>>> parent of 0519859... place_functions, arbeit am Hub
=======
>>>>>>> parent of 0519859... place_functions, arbeit am Hub
def get_places():
	try:
		return functions.get_gamedata()["places"];
	except:
		return {};
def get_place(name):
	return get_places()[name];
def save_places(array):
	functions.add_json_string("user\gamedata.json", "places", array);