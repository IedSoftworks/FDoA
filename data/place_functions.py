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
def get_places():
	try:
		return functions.get_gamedata()["places"];
	except:
		return {};
def get_place(name):
	return get_places()[name];
def save_places(array):
	functions.add_json_string("user\gamedata.json", "places", array);