from data import event_functions
from data import functions
from data import gui_content
from data import factions
from tkinter import *;
from functools import partial;
from data import place_functions;

class init():
	def __init__(self, gui, arg=[]):
		gui.hubstorage = self;
		self.gui = gui;
		self.hintergrund = self.gui.hintergrund();
		self.hintergrund.pack();
		self.hintergrund.after(0, self.hub_menu);
		self.hintergrund.mainloop();
	
	def clear_screen1(self):
		self.hintergrund.forget();
		self.hintergrund = self.gui.hintergrund();
		self.hintergrund.pack();
	
	def hub_menu(self):
		gd = functions.get_gamedata();
		self.clear_screen1();
		menu = Canvas(self.hintergrund, bg="gold2", highlightthickness=0);
		menu.place(x=functions.pro_size(5,0), y=functions.pro_size(5,1));
		Button(menu, text="Inventar", command=self.inventory, width=functions.pro_size(1,0), font=gui_content.ch_fontsize(16)).grid(row=1);
		check=True;
		try:
			exec("print(\""+str(gd["travel"])+"\")");
		except:
			check=False;
		if check:
			Label(menu, text="Aktuelle Reise: \nZiel: "+gd["travel"]["destination"]+"\nAnkunft in: "+str(gd["travel"]["steps"]), bg="Gold2", font=gui_content.ch_fontsize(16)).grid(row=1,column=1,sticky=W);
		else:
			Label(menu, text="Aktuelle Reise: \nKeine", bg="Gold2", font=gui_content.ch_fontsize(16)).grid(row=1,column=1,sticky=W);
			Button(menu, text="Ort ansteuern", command=self.travel, font=gui_content.ch_fontsize(16)).grid(row=2,column=1,sticky=W);
		Button(menu, text="Fraktions-Übersicht", command=self.factions, font=gui_content.ch_fontsize(16)).grid(row=1,column=2,sticky=W);
		
		Button(self.hintergrund, text="Weiter gehen", command=self.hintergrund.quit, font=gui_content.ch_fontsize("16")).place(x=functions.pro_size(50,0), y=functions.pro_size(85,1), anchor=CENTER);
	
	def inventory(self):
		self.clear_screen1();
		hintergrund = self.hintergrund;
		
		Label(hintergrund, text="Inventar", font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);
		Button(hintergrund, text="Zurück", command=self.hub_menu, font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(5,1), x=functions.pro_size(50,0), anchor=N);
		
		inventar1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		inventar1.place(anchor=N, x=functions.pro_size(50,0), y=functions.pro_size(10,1));
		inventar = functions.VerticalScrolledFrame(inventar1);
		inventar.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		
		inventar_content = functions.get_inventory();
		if len(inventar_content) == 0:
			Label(inventar.interior, text="Keine Items", font=gui_content.ch_fontsize("32")).place(x=functions.pro_size(50,0), y=functions.pro_size(50,1), anchor=CENTER);
		else:
		
			xrow = 0;
			for inv, value in inventar_content.items():
				xrow +=1
				setattr(self, "inv_canvas"+str(xrow), Canvas(inventar.interior, bg="green", width=functions.pro_size(90,0), height=functions.pro_size(9,1)));
				getattr(self, "inv_canvas"+str(xrow)).grid(row=xrow);
				Label(getattr(self, "inv_canvas"+str(xrow)), text=inv, font=gui_content.ch_fontsize("40"), bg="green", fg="white").place(x=functions.pro_size(1,0), y=functions.pro_size(4.5,1), anchor=W);
				Label(getattr(self, "inv_canvas"+str(xrow)), text="Anzahl: "+str(value), fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(88,0), anchor=SE);
				Button(getattr(self, "inv_canvas"+str(xrow)), command=partial(self.useitem, inv), text="Verwenden", fg="white",bg="green").place(y=functions.pro_size(9,1), x=functions.pro_size(78,0), anchor=SE);
	def travel(self):
		place_functions.enterveh(self.gui, {"name":"selfdestruct","steps":100,"events":"all"}, self, -1);
	def factions(self):
		factions.overview(self.gui, self);
	def useitem(self, item):
		hintergrund = self.hintergrund;

		Text = Canvas(hintergrund, bg="Gold2", highlightthickness=0, width=functions.pro_size(28,0), height=functions.pro_size(28,1));
		Text.place(x=functions.pro_size(36,0), y=functions.pro_size(36,1));
		Text2 = Canvas(hintergrund, bg="Gold2", highlightthickness=0, width=functions.pro_size(20,0), height=functions.pro_size(20,1));
		Text2.place(x=functions.pro_size(40,0), y=functions.pro_size(40,1));

		Button(Text2, text="Zurück", command=self.inventory).grid(row=0,column=1,padx=5,pady=5);
		x = 1;
		y = 1;
		if not hasattr(self.gui, "itemevents"):
			setattr(self.gui, "itemevents", {});
		if not item in self.gui.itemevents:
			self.gui.itemevents[item]={};
		for button, event in self.gui.itemevents[item].items():
			notbutton=False;
			if "place" in event:
				if not event["place"] == functions.get_gamedata()["place"]:
					notbutton=True;
			if not notbutton:
				Button(Text2, text=button, command=partial(self.useitem2, item, event[1], event[0])).grid(row=y,column=x,padx=5,pady=5);
			x+=1;
			if x == 6:
				x = 1;
				y += 1;
	def useitem2(self, item, event1, event0):
		self.gui.hook.onItemAction.fire(item, event0, event1);
		self.gui.game(event1, event0);