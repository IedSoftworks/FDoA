from data import functions;
from data import event_functions;
from data import gui_content;
import random;
import hashlib;
from tkinter import *
from functools import partial;

def register(data, override=False):
	from data.getgui import gui;
	quests = get_quests();
	id = random.random() * 1000000;
	id = hashlib.md5(str(id).encode('utf-8')).hexdigest();
	data["id"]=id;
	if not "title" in data:
		data["title"]="Quest";
	if not "description" in data:
		data["description"]="";
	if not "sdescription" in data:
		data["sdescription"]=data["title"]+"\n"+data["description"];
	if not "tools" in data:
		data["tools"]={};
	if not "rewards" in data:
		data["rewards"]={};
	if not "requirements" in data:
		data["requirements"]={};
	quests[id]=data;
	gd = functions.get_gamedata();
	save=True;
	if "quests" in gd:
		if "bind" in gd["quests"]:
			if gui.last_event[0]+"+"+gui.last_event[1]+"+"+data["title"] in gd["quests"]["bind"] and not override:
				save=False;
	if save:
		gd["quests"]=quests;
		if not "bind" in gd["quests"]:
			gd["quests"]["bind"]={};
			gd["quests"]["active"]=[];
		gd["quests"]["bind"][gui.last_event[0]+"+"+gui.last_event[1]+"+"+data["title"]]=id;
		functions.save_gamedata(gd);
		gui.hook.onQuestRegister.fire(data);
def questmenu(title, decline=False, accept=False, finish=False, cancelfunc=False, confunc=False):
	from data.getgui import gui;
	if not decline:
		decline=gui.new_text;
	if not accept:
		accept=gui.new_text;
	if not finish:
		finish=gui.new_text;
	if not cancelfunc:
		cancelfunc=gui.new_text;
	if not confunc:
		confunc=gui.new_text;
	gd = functions.get_gamedata();
	id = gd["quests"]["bind"][gui.last_event[0]+"+"+gui.last_event[1]+"+"+title];
	quest=get_quests()[id];
	reached=False;
	active=False;
	if id in gd["quests"]["active"]:
		reached=True;
		for item, amount in quest["requirements"].items():
			if event_functions.check_item(item) < amount:
				reached=False;
		active=True;
	gui.clear_screen();
	back = gui.hintergrund();
	back.pack();
	Text = Canvas(back, bg="Gold2", highlightthickness=0, width=functions.pro_size(80,0));
	Text.place(x=functions.pro_size(10,0), y=functions.pro_size(10,1));
	Label(Text, text="Quest:", font=gui_content.ch_fontsize(12), bg="Gold2").grid(row=0,columnspan=3,sticky=W);
	Label(Text, text=quest["title"], font=gui_content.ch_fontsize(32), bg="Gold2").grid(row=1,columnspan=3,sticky=W);
	Label(Text, text=quest["description"], font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=2,columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=3,columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=4,columnspan=3,sticky=W);
	Label(Text, text="Zu beschaffende Items:", font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=50,sticky=W);
	i=49;
	for item, amount in quest["requirements"].items():
		i+=1;
		Label(Text, text=item+" x "+str(amount), font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=i,column=2,sticky=W);
	i+=1;
	Label(Text, text="Erhaltene Items zum Erfüllen der Quest:", font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=i,columnspan=2,sticky=W);
	i-=1;
	for item, amount in quest["tools"].items():
		i+=1;
		Label(Text, text=item+" x "+str(amount), font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=i,column=2,sticky=W);
	i+=1;
	Label(Text, text="Belohnungen:", font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=i,sticky=W);
	i-=1;
	for item, amount in quest["rewards"].items():
		i+=1;
		Label(Text, text=item+" x "+str(amount), font=gui_content.ch_fontsize(16), bg="Gold2").grid(row=i,column=2,sticky=W);
	i+=1;
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=i,columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=(i+1),columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=(i+2),columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=(i+3),columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=(i+4),columnspan=3,sticky=W);
	Label(Text, text="a", font=gui_content.ch_fontsize(16), bg="Gold2", fg="Gold2").grid(row=(i+5),columnspan=3,sticky=W);
	i+=6;
	nobutton=True;
	if not active:
		if not gd["quests"]["active"]:
			Button(Text, text="Annehmen", command=partial(acceptquest, accept, quest), bg="green", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,column=0,padx=5,pady=5);	
			Button(Text, text="Ablehnen", command=partial(declinequest, decline, quest), bg="red", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=1);	
			nobutton=False;
		else:	
			Button(Text, text="Beende zuerst deine aktuelle Quest!", state=DISABLED, bg="red", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=0);		
	elif reached:		
		Button(Text, text="Erreicht!", state=DISABLED, bg="green", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=0);	
		Button(Text, text="Belohnung abholen", command=partial(get, quest, finish), bg="green", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=1);	
	else:
		Button(Text, text="Aktiv", state=DISABLED, bg="blue", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=0);	
		Button(Text, text="Abbrechen", command=partial(cancel, quest, cancelfunc), bg="red", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=1);	
	if nobutton:
		Button(Text, text="Weiter", command=confunc, bg="white", font=gui_content.ch_fontsize("16"), width=functions.pro_size(1,0)).grid(row=i,padx=5,pady=5,column=10);	
		
def get_quests():
	try:
		return functions.get_gamedata()["quests"];
	except:
		return {};
def acceptquest(func, quest):
	from data.getgui import gui;
	gui.hook.onQuestAccept.fire(quest);
	event_functions.add_items(quest["tools"]);
	gd = functions.get_gamedata();
	gd["quests"]["active"].append(quest["id"]);
	functions.save_gamedata(gd);
	func();
def declinequest(func, quest):
	from data.getgui import gui;
	gui.hook.onQuestDecline.fire(quest);
	func();
def get(quest, func):
	from data.getgui import gui;
	gui.hook.onQuestFinish.fire(quest);
	gd = functions.get_gamedata();
	gd["quests"]["active"].remove(quest["id"]);
	functions.save_gamedata(gd);
	event_functions.add_items(quest["rewards"]);
	for item, amount in quest["requirements"].items():
		event_functions.remove_items(item, amount);
	func();
def cancel(quest, func):
	from data.getgui import gui;
	gui.hook.onQuestCancel.fire(quest);
	gd = functions.get_gamedata();
	gd["quests"]["active"].remove(quest["id"]);
	functions.save_gamedata(gd);
	func();