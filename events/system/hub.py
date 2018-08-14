from data import event_functions
from data import functions
from data import gui_content
from data import factions
from tkinter import *;
from functools import partial;
from data import place_functions;

class init():
	def __init__(self, gui):
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
			Button(menu, text="Ort ansteuern", command=partial(place_functions.enterveh, self.gui, {"name":"selfdestruct","steps":100,"events":"all"}), font=gui_content.ch_fontsize(16)).grid(row=2,column=1,sticky=W);
		Button(menu, text="Fraktions-Übersicht", command=partial(factions.overview, self.gui), font=gui_content.ch_fontsize(16)).grid(row=1,column=2,sticky=W);
		
		Button(self.hintergrund, text="Weiter gehen", command=self.hintergrund.quit, font=gui_content.ch_fontsize("16")).place(x=functions.pro_size(50,0), y=functions.pro_size(85,1), anchor=CENTER);
	
	def inventory(self):
		self.hintergrund.quit();
		self.gui.clear_screen();
		hintergrund = self.gui.hintergrund();
		hintergrund.pack();
		
		Label(hintergrund, text="Inventar", font=gui_content.ch_fontsize("16"), bg="green"). place(y=functions.pro_size(1,1), x=functions.pro_size(50,0), anchor=N);
		
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
			
			