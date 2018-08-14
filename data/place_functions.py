import random;
import os;
import collections;
from data import functions;
from data import gui_content
from data import container;
from tkinter import *;
from tkinter import font;
import math;
from functools import partial
import types

def register(data, override=False):
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
		exec("print("+str(data["garage"])+")");		#
	except:										#
		check = False;							#
	if not check:									#
		place["garage"] = {"storage":{},"size":1,"disable":False};	#
	else:											#
		place["garage"] = data["garage"];		#
	# --#										#
	check = True;								#
	try:										#
		exec("print("+data["word"]+")");		#
	except:										#
		check = False;							#
	if not check:								#
		place["word"] = "in";					#
	else:										#
		place["word"] = data["word"];		#
	# --#										#
	check = True;								#
	try:										#
		exec("print("+str(data["storage"])+")");		#
	except:										#
		check = False;							#
	if not check:									#	
		place["storage"] = {"storage":{},"size":8,"disable":False};#
	else:											#
		place["storage"] = data["storage"];		#
	# --#										#
	check = True;								#
	try:										#
		exec("print("+str(data["description"])+")");		#
	except:										#
		check = False;							#
	if not check:								#	
		place["description"] = ""				#
	else:										#
		place["description"] = data["description"];	#
	# --#										#
	
	con = container.register({"inv":place["storage"]["storage"],"name":"Lager von "+data["name"],"size":place["storage"]["size"]});
	place["system"] = {"first":True,"container":con};
	check=False;
	try:
		exec("print(\""+str(placejson[data["name"]])+"\")");
	except:
		check=True;
	if check or override:
		placejson[data["name"]] = place;
	save_places(placejson);
def enterplace(gui, name, takeveh=False, endjourney=False, force=False):
	gd = functions.get_gamedata();
	place = get_place(name);
	check=True;
	try:
		exec("print(\""+str(gd["travel"])+"\")");
	except KeyError:
		check=False;
	stop=False;
	if check:
		if gd["travel"]["destination"]==name and not endjourney and not force:
			stop=True;
	if not stop:
		gd["place"] = name;
		gd["place_hub_timer"]=0;
		if endjourney:
			veh = gd["travel"]["vehicle"];
			del gd["travel"];
		elif takeveh:
			veh = gd["travel"]["vehicle"];
		garageworks=True;
		try:
			if veh["name"]=="selfdestruct":
				takeveh=False;
		except UnboundLocalError:
			print("");
		if takeveh:
			garageworks=False;
			if len(gd["places"][name]["garage"]["storage"]) >= gd["places"][name]["garage"]["size"]:
				functions.save_gamedata(gd);
				garageerror(gui, veh);
			else:
				gd["places"][name]["garage"]["storage"].append(veh);
				garageworks=True;
		if garageworks:
			if place["system"]["first"] and place["options"]["events"]["enterf"][0] != "None":
				gd["places"][name]["system"]["first"] = False;
				functions.save_gamedata(gd);
				gui.game(place["options"]["events"]["enterf"][1], place["options"]["events"]["enterf"][0], ["place-enterf", name]);
			else:
				functions.save_gamedata(gd);
				if place["options"]["events"]["entern"][0] != "None":
					gui.game(place["options"]["events"]["entern"][1], place["options"]["events"]["entern"][0], ["place-entern", name]);
				else:
					hub(gui, False, True);
	else:
		gui.new_text();
def hub(gui, travel=False, returned=False):
	gui.clear_screen();
	back = gui.hintergrund();
	back.pack();
	gd = functions.get_gamedata();
	if travel:
		print(gd["travel"]["steps"]);
		if gd["travel"]["steps"] <= 0:
			print("Destination Reached.");
			enterplace(gui, gd["travel"]["destination"], True, True);
		else:
			gd["travel"]["steps"]-=1;
			functions.save_gamedata(gd);
			print("Travel");
			event(gui, gd["travel"]["vehicle"]["events"]);
	else:
		try:
			place = get_place(gd["place"]);
		except KeyError:
			gui.game("hub","system");
		try:
			exec("print(\""+str(gd["place_hub_timer"])+"\")");
		except:
		#	print(sys.exc_info());
			gd["place_hub_timer"] = 0;
		print(gd["place_hub_timer"]);
		if not returned:
			if not gd["place_hub_timer"] == 0:
				if not gd["place_hub_timer"] >= (place["options"]["hubtimer"]+1):
					gd["place_hub_timer"]+=1;
					functions.save_gamedata(gd);
					print("Random");
					event(gui, place["options"]["events"]["random"]);
				else:
					print(str(place["options"]["hubtimer"]+1)+"/"+str(gd["place_hub_timer"]));
					gd["place_hub_timer"]=0;
					functions.save_gamedata(gd);
			gd["place_hub_timer"]+=1;
		functions.save_gamedata(gd);
		Text = Canvas(back, bg="Gold2", highlightthickness=0);
		Text.place(x=functions.pro_size(10,0), y=functions.pro_size(10,1));
		Label(Text, text="Willkommen "+place["word"]+" "+gd["place"], font=gui_content.ch_fontsize(32), bg="Gold2").grid(row=1,columnspan=3,sticky=W);
		Button(Text, text="Garage", command=partial(garage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,padx=5,pady=5);
		if not place["storage"]["disable"]:
			Button(Text, text="Lager", command=partial(storage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,column=1,padx=5,pady=5);
		else:
			Button(Text, text="Lager", state=DISABLED, command=partial(storage, gui), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,column=1,padx=5,pady=5);
		if not gd["place"] in get_gps():
			Button(Text, text="Ort Speichern", command=partial(savetogps, gui, place), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=2,column=2,padx=5,pady=5);
		else:			
			Button(Text, text="Ort Gespeichert.", command=partial(print, ""), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0), bg="green").grid(row=2,column=2,padx=5,pady=5);
		if len(place["options"]["events"]["clickable"]) > 0:
			Label(Text, text="Aktionen:", font=gui_content.ch_fontsize(20), bg="Gold2").grid(row=3,sticky=W,columnspan=3);
			key = 0;
			for value in place["options"]["events"]["clickable"]:
				row = math.floor(key / 6) + 4;
				column = (key % 6);
				if key < 61:
					Button(Text, text=value[2], command=partial(clickable, gui, value), font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0), height=functions.pro_size(.05,1)).grid(row=row,column=column,padx=5,pady=5);
				elif key == 61:
					Label(Text, text="Maximum von 60 Aktionen überschritten.", font=gui_content.ch_fontsize(20), bg="Gold2", fg="red").grid(row=14,sticky=W,columnspan=6);	
				key+=1;	
		Label(Text, text=place["description"], font=gui_content.ch_fontsize(20), bg="Gold2").grid(row=15,sticky=W,columnspan=3);
		Button(Text, text=gd["place"]+" verlassen", command=partial(leave, gui), bg="red", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=16,padx=5,pady=5);	
		if len(place["options"]["events"]["random"]) > 0:
			Button(Text, text="Weitergehen", command=partial(event, gui, place["options"]["events"]["random"]), bg="green", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=16,column=1,padx=5,pady=5);	
		else:
			Button(Text, text="Weitergehen", state=DISABLED, command=partial(event, gui), bg="green", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=16,column=1,padx=5,pady=5);		
def savetogps(gui, place, remkey=-1):
	gd = functions.get_gamedata();
	try:
		gpsmax = gd["gpsmax"];
	except:
		gpsmax = 3;
		gd["gpsmax"] = 3;
	gps = get_gps();
	if len(get_gps()) < gpsmax:
		gps.append(gd["place"]);
		gd["gps"]=gps;
		functions.save_gamedata(gd);
		print("success");
	else:
		if not remkey == -1:
			print("replaced");
			gps[remkey]=gd["place"];
			gd["gps"]=gps;
			functions.save_gamedata(gd);
		else:
			print("full");
			enterveh(gui, place, True, -2);
	hub(gui);
def garage(gui):
		gui.clear_screen();
		hintergrund = gui.hintergrund();
		hintergrund.pack();
		
		Label(hintergrund, text="Garage von "+functions.get_gamedata()["place"], font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);
		Button(hintergrund, text="Zurück", command=partial(hub, gui, False, True), font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(5,1), x=functions.pro_size(50,0), anchor=N);
		
		inventar1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		inventar1.place(anchor=N, x=functions.pro_size(50,0), y=functions.pro_size(10,1));
		inventar = functions.VerticalScrolledFrame(inventar1);
		inventar.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		
		inventar_content = get_place(functions.get_gamedata()["place"])["garage"]["storage"];
		if len(inventar_content) == 0:
			Label(inventar.interior, text="Leer", font=gui_content.ch_fontsize("32")).place(x=functions.pro_size(50,0), y=functions.pro_size(50,1), anchor=CENTER);
		else:
		
			xrow = 0;
			for value in inventar_content:
				xrow +=1
				newcanvas = {};
				newcanvas[xrow] = Canvas(inventar.interior, bg="green", width=functions.pro_size(90,0), height=functions.pro_size(9,1));
				newcanvas[xrow].grid(row=xrow);
				Label(newcanvas[xrow], text=value["name"], font=gui_content.ch_fontsize("40"), bg="green", fg="white").place(x=functions.pro_size(1,0), y=functions.pro_size(4.5,1), anchor=W);
				Button(newcanvas[xrow], text="Benutzen", command=partial(enterveh, gui, value, True, (xrow-1)), fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);
def storage(gui):
	container.openxx(get_place(functions.get_gamedata()["place"])["system"]["container"], gui); 
def enterveh(gui, vehicle, self, key=-1):
		if isinstance(self, bool):
			gui.clear_screen();
			hintergrund = gui.hintergrund();
			hintergrund.pack();
			ishub=False;
		else:
			print("Baum");
			self.clear_screen1();
			hintergrund = self.hintergrund;
			ishub=True;
		gui.placeback = self;
		
		if key == -2:
			Label(hintergrund, text="Dein GPS ist voll. Bitte wähle einen Eintrag, den du ersetzen möchtest.", font=gui_content.ch_fontsize("24"), bg="red"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);
		else:	
			Label(hintergrund, text="GPS-Einträge", font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);
		if ishub:
			Button(hintergrund, text="Abbrechen", command=self.hub_menu, font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(6,1), x=functions.pro_size(50,0), anchor=N);
		else:			
			Button(hintergrund, text="Abbrechen", command=partial(hub, gui, False, True), font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(6,1), x=functions.pro_size(50,0), anchor=N);
		inventar1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		inventar1.place(anchor=N, x=functions.pro_size(50,0), y=functions.pro_size(10,1));
		inventar = functions.VerticalScrolledFrame(inventar1);
		inventar.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		
		inventar_content = get_gps();
		if len(inventar_content) == 0:
			Label(inventar.interior, text="Leer", fg="black", font=gui_content.ch_fontsize("32")).place(x=functions.pro_size(50,0), y=functions.pro_size(50,1), anchor=CENTER);
		else:
		
			xrow = 0;
			for value in inventar_content:
				xrow +=1
				newcanvas = {};
				newcanvas[xrow] = Canvas(inventar.interior, bg="green", width=functions.pro_size(90,0), height=functions.pro_size(9,1));
				newcanvas[xrow].grid(row=xrow);
				Label(newcanvas[xrow], text=value, font=gui_content.ch_fontsize("40"), bg="green", fg="white").place(x=functions.pro_size(1,0), y=functions.pro_size(4.5,1), anchor=W);
				if not key == -2:
					Button(newcanvas[xrow], text="Reisen ["+str(vehicle["steps"])+"]", command=partial(travel, gui, value, vehicle, key), fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);
				else:
					Button(newcanvas[xrow], text="Ersetzen", command=partial(savetogps, vehicle, (xrow-1)), fg="white",bg="red").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);					
def event(gui, events):
	gd = functions.get_gamedata();
	event = random.SystemRandom().choice(events);
	keyword="random";
	try:
		exec("print(\""+gd["place"]+"\")");
	except:
		gd["place"]="";
		keyword="travel";
	gui.game(event[1], event[0], ["place-"+keyword, gd["place"]]);
def leave(gui):
	gd = functions.get_gamedata();
	try:
		place = get_place(gd["place"]);
		del gd["place"];
		functions.save_gamedata(gd);
		if place["options"]["events"]["exit"][0] != "None":
			gui.game(place["options"]["events"]["exit"][1], place["options"]["events"]["exit"][0], ["place-exit", name]);
		else:
			gui.new_text();
	except:
		gui.new_text();
def garageerror(gui, veh):
	gui.clear_screen();
	back = gui.hintergrund();
	back.pack();
	gd = functions.get_gamedata();
	
	Label(back, text="Die Garage von "+gd["place"]+"ist voll.", bg="Gold2", fg="red", font=gui_content.ch_fontsize("32")).grid(row=1, column=1, columnspan=2, sticky=NSEW)
	Button(back, text="Fahrzeug "+veh["name"]+" zerstören.", command=partial(hub, gui), font=gui_content.ch_fontsize("16"), bg="green").grid(row=2, column=1, sticky=NSEW)
	Button(back, text="Zu einem anderen Ort fahren.", command=partial(enterveh, gui, veh), font=gui_content.ch_fontsize("16"), bg="green").grid(row=2, column=2, sticky=NSEW)

	back.grid_rowconfigure(0, weight=1)
	back.grid_rowconfigure(3, weight=1)
	back.grid_columnconfigure(0, weight=1)
	back.grid_columnconfigure(3, weight=1)
def travel(gui, place, vehicle, key=-1):
	gd = functions.get_gamedata();
	vehicle["key"]=key;
	gd["travel"] = {"steps":vehicle["steps"],"destination":place,"vehicle":vehicle};
	if not key == -1:
		del gd["places"][gd["place"]]["garage"]["storage"][key];
	functions.save_gamedata(gd);
	leave(gui);
def clickable(gui, event):
	gd = functions.get_gamedata();
	gui.game(event[1], event[0], ["clickable", gd["place"]]);
def get_places():
	try:
		return functions.get_gamedata()["places"];
	except:
		return {};
def get_gps():
	try:
		return functions.get_gamedata()["gps"];
	except:
		return [];
def get_place(name):
	return get_places()[name];
def save_places(array):
	functions.add_json_string("user\gamedata.json", "places", array);