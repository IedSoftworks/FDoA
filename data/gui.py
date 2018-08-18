import os;
import sys;
from tkinter import *;
from functools import partial;
from data import functions;
from data import gui_content;
from data import event_functions;
import ctypes
import random
import inspect
from data import place_functions;

class GUI():
	#System Start
	def __init__(self):
		self.root = Tk();
		self.root.title("Four Dragons of Apocalypse Test-PreAlpha | Ied Softworks");
		self.root.geometry(str(functions.get_screensize(0))+"x"+str(functions.get_screensize(1)));
		self.content_frame = Frame(self.root);
		self.content_frame.pack();
		self.state = True
		self.root.attributes("-fullscreen", True);
		self.root.bind("<F11>", self.toggle_fullscreen);
		self.root.bind("<F4>", self.ending_game);

	def system_start(self, mod):
		self.activemod = mod;
		self.content_frame.after(0, self.main_menu)
		self.content_frame.mainloop();

	def debug(self):
		self.clear_screen();
		Label(self.content_frame, text="Folder:").pack();
		fold = Entry(self.content_frame);
		fold.pack();
		Label(self.content_frame, text="File:").pack();
		x = Entry(self.content_frame);
		x.pack();
		Label(self.content_frame, text="Arguments: Spaterate with \"/\"(Keep clear, if you don't need Arguments)").pack();
		self.arg = Entry(self.content_frame);
		self.arg.pack();

		def run(event=None):
			folder = fold.get();
			file = x.get();
			arg = self.arg.get();
			self.root.unbind("<Return>");
			if len(folder) == 0:
				folder = "main"
			if arg != "":
				arg1 = arg.split("/");
				self.game(file, folder,arg1);
			else:
				self.game(file, folder);

		self.root.bind("<Return>", run);

		Button(self.content_frame, text="Run Event", command=run).pack();
		Button(self.content_frame, text="Back to the Roots ... ähm Main-Menu", command=self.main_menu).pack();
		self.root.bind("<F12>", self.main_menu);

	def main_menu(self, event=None):
		self.clear_screen();
		hintergrund1 = self.hintergrund();
		Button(hintergrund1, text="DEBUG", command=self.debug, bd=0, bg="gold2", fg="gold2").place(y=0);
		Label(hintergrund1, font=gui_content.ch_fontsize("32"), text="Four Dragons of Apocalypse").place(y=75, x=functions.pro_size(50,0), anchor=CENTER);

		if self.activemod != "main":
			Label(hintergrund1, text=self.activemod, font=gui_content.ch_fontsize("24")).place(y=125, x=functions.pro_size(50,0), anchor=CENTER);

		Button(hintergrund1, text="Update", bd=8,font=gui_content.ch_fontsize("16"),bg="blue", fg="white", command=self.update).place(anchor=NE, y=functions.pro_size(1,1), x=functions.pro_size(99,0));
		Button(hintergrund1, text="Start", font=gui_content.ch_fontsize("20"),bg="green", fg="white", bd=8,command=self.caracter_choose).place(anchor=CENTER, y=functions.pro_size(20,1), x=functions.pro_size(50,0), width=functions.pro_size(25, 0), height=functions.pro_size(10, 1));
		Button(hintergrund1, text="Mods", font=gui_content.ch_fontsize("20"),bg="red", fg="white", bd=8,command=self.modmanager).place(anchor=CENTER, y=functions.pro_size(35,1), x=functions.pro_size(50,0), width=functions.pro_size(25, 0), height=functions.pro_size(10, 1));
		Button(hintergrund1, text="Beenden", font=gui_content.ch_fontsize("20"),bg="blue", fg="white", bd=8,command=self.ending_game).place(anchor=CENTER, y=functions.pro_size(50,1), x=functions.pro_size(50,0), width=functions.pro_size(25, 0), height=functions.pro_size(10, 1));
		Label(hintergrund1, text="Beta-Testers:\n\n"+functions.read_file_content("data\BetaTester.txt"), bg="gold2", font=gui_content.ch_fontsize("16")).place(y=functions.pro_size(100,1), x=functions.pro_size(0,1), anchor=SW);

		hintergrund1.pack();
		self.content_frame.mainloop();

	"""
	def game_choose(self):
		self.clear_screen();
		hintergrund1 = Canvas(self.content_frame, bg="Gold2", width=900, height=800);
		if os.path.exists("user\gamedata1.json"):
			file = functions.json_file_decode("user\\gamedata1.json");
			gui_content.button(hintergrund1, "Game 1: "+file["name"], 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);
		else:
			gui_content.button(hintergrund1, "Game 1: LEER", 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);
		if os.path.exists("user\gamedata2.json"):
			file = functions.json_file_decode("user\\gamedata1.json");
			gui_content.button(hintergrund1, "Game 2: "+file["name"], 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);
		else:
			gui_content.button(hintergrund1, "Game 2: LEER", 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);
		if os.path.exists("user\gamedata3.json"):
			file = functions.json_file_decode("user\\gamedata3.json");
			gui_content.button(hintergrund1, "Game 3: "+file["name"], 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);
		else:
			gui_content.button(hintergrund1, "Game 3: LEER", 400, 480, exist_game_1, gui_content.ch_fontsize("16"), "green", "black"], [100,50]);

		self.root.mainloop();
	"""

	def modmanager(self):
		class init():
			def __init__(self):
				true = True;

		init = init();
		self.clear_screen();
		hintergrund = self.hintergrund();
		hintergrund.pack();

		hintergrund1 = Canvas(hintergrund, width=functions.pro_size(90,0), height=functions.pro_size(80,1));
		hintergrund1.place(y=functions.pro_size(15,1), x=functions.pro_size(5,0))
		modlist = functions.VerticalScrolledFrame(hintergrund1);
		modlist.place(width=functions.pro_size(90,0), height=functions.pro_size(80,1));

		folders = [f.path for f in os.scandir("events") if f.is_dir() ]
		folder = [x[7:] for x in folders];

		def activate(self, mod):
			self.activemod = mod;
			self.main_menu();

		xrow = 1
		setattr(init, "canvas"+str(xrow), Canvas(modlist.interior, bg="blue", width=functions.pro_size(45,0), height=functions.pro_size(10,1)));
		getattr(init, "canvas"+str(xrow)).grid(row=xrow);
		Label(getattr(init, "canvas"+str(xrow)), bg="blue", text="main", font=gui_content.ch_fontsize("32")).place(x=5, y=5);
		if self.activemod == "main":
			Label(getattr(init, "canvas"+str(xrow)), text="Activ", font=gui_content.ch_fontsize("16"), fg="yellow", bg="blue").place(x=5, y=50);
		else:
			Button(getattr(init, "canvas"+str(xrow)), text="Aktivieren", bg="navy", command=partial(activate, self, "main"), fg="white", font=gui_content.ch_fontsize("16")).place(x=functions.pro_size(45,0), y=5, anchor=NE);

		for f in folder:
			xrow +=1
			if f != "__pycache__":
				if f != "system":
					if f != "main":
						setattr(init, "canvas"+str(xrow), Canvas(modlist.interior, bg="blue", width=functions.pro_size(45,0), height=functions.pro_size(10,1)));
						getattr(init, "canvas"+str(xrow)).grid(row=xrow);
						Label(getattr(init, "canvas"+str(xrow)), bg="blue", text=f, font=gui_content.ch_fontsize("32")).place(x=5, y=5);
						if self.activemod == f:
							Label(getattr(init, "canvas"+str(xrow)), text="Activ", font=gui_content.ch_fontsize("16"), fg="yellow", bg="blue").place(x=5, y=50);
						else:
							Button(getattr(init, "canvas"+str(xrow)), text="Aktivieren", bg="navy", command=partial(activate, self, f), fg="white", font=gui_content.ch_fontsize("16")).place(x=functions.pro_size(45,0), y=5, anchor=NE);

	def caracter_choose(self):
		self.clear_screen();
		caracters = functions.json_file_decode("content\persons.json");
		current_car = functions.json_file_decode("user\\avapersons.json");
		dic = functions.json_file_decode("user\\found_description.json");
		hintergrund1 = self.hintergrund();

		gio = Frame(hintergrund1);
		carder = functions.VerticalScrolledFrame(gio);
		carder.interior.config(height=functions.pro_size(30,0))
		carder.config(bg="LightCyan3", bd=8, highlightbackground="orange3");

		def choose_caracter(gg):
			self.selected_caracter = gg;
			print(self.selected_caracter);
			selected_caracter_name.config(text=self.selected_caracter);
			if not self.selected_caracter in dic:
				story = "<!Geschichte nicht erforscht!>";
			else:
				story = caracters[gg]["story"];
			selected_caracter_disc.config(text="Geschichte: \n"+story);

		X = 0;
		ypos = X;
		ypos_pic = 10;
		rowx = 1
		caracter_canvas = {};
		car_checkbox={};
		xd = 0;
		for key, value in caracters.items():
			if key in current_car:
				try:
					value["img"];
				except:
					value["img"]="noimage";
				abil = "";
				for y in range(len(value["abilitys"])):
					abil += value["abilitys"][y]+", ";
				abil = abil[:-2];
				yx = Canvas(carder.interior, bg="green4", height=100, width=660, bd=15, highlightbackground="yellow");
				img = Canvas(yx, width=100, height=100);
				setattr(self, "car"+str(X)+"_background_img", PhotoImage(file="content\pictures\\background_car.gif"))
				setattr(self, "car"+str(X)+"_img", PhotoImage(file = "content\pictures\\"+value["img"]+".gif"));
				#img.create_image(image=getattr(self, "car"+str(X)+"_img"), 90, 90)
				img.create_image(100, 100, image=getattr(self, "car"+str(X)+"_background_img"))
				Label(yx, text=key, bg="green4", font=gui_content.ch_fontsize("30")).place(x=110, y=10);
				Label(yx, text="Spezies/Rasse: "+value["species"], font=gui_content.ch_fontsize("16"), bg="green4").place(x=110, y=55);
				Label(yx, text="Fähigkeiten: "+abil, font=gui_content.ch_fontsize("16"), bg="green4").place(x=110, y=80);

				setattr(self, "car"+str(X)+"_choose_caracter", partial(choose_caracter, key));
				car_checkbox[X] = IntVar();
				gui_content.button(yx, "Select", 600, 10, getattr(self, "car"+str(X)+"_choose_caracter"), gui_content.ch_fontsize("16"), ["green", "black"], [90, 30]);

				yx.pack();
				ypos += 210
				rowx += 1
				X += 1;

		def start_game():
			self.gamedata = {};
			self.gamedata["caracters"]={};
			self.gamedata["caracters"][self.selected_caracter]={"hp":functions.get_persons_content()[self.selected_caracter]["stdhp"]}
			functions.json_file_encode("user\gamedata.json", self.gamedata);
			self.hub_time = 2;
			try:
				items = functions.get_persons_content()[self.selected_caracter]["stditems"]
			except:
				items = {};
			items["coins"] = 300
			event_functions.add_items(items);
			self.game("startgame", "system", [self.selected_caracter]);

		selected_caracter_name = Label(hintergrund1, text="Niemand", font=gui_content.ch_fontsize("16"), bg="Gold2");
		selected_caracter_name.place(y=functions.pro_size(40,1), x=functions.pro_size(50,0), anchor=N);
		selected_caracter_disc = Message(hintergrund1, text="Geschichte: \n", bg="Gold2", font=gui_content.ch_fontsize("14") ,width=600);
		selected_caracter_disc.place(y=functions.pro_size(50,1), x=functions.pro_size(50,0), anchor=N);

		Button(hintergrund1, text="Zurück", command=self.main_menu, bg="red", bd=8, font=gui_content.ch_fontsize("20")).place(anchor=W, y=functions.pro_size(75,1), x=functions.pro_size(25,0), width=functions.pro_size(25,1), height=functions.pro_size(10,0))
		Button(hintergrund1, text="START!!!!", command=start_game, bg="green", bd=8, font=gui_content.ch_fontsize("20")).place(anchor=E, y=functions.pro_size(75,1), x=functions.pro_size(75,0), width=functions.pro_size(25,1), height=functions.pro_size(10,0))

		hintergrund1.pack()
		gio.place(y=functions.pro_size(5,1), x=functions.pro_size(50,0), anchor=N);
		carder.pack();
		self.content_frame.mainloop();

	def game(self, game_file, game_folder=False, game_arg="none", await_return = False):
		self.clear_screen();

		if not game_folder:
			game_folder1 = str(inspect.stack()[1][1])
			game_folder1 = game_folder1.split("\\");
			game_folder1 = game_folder1[len(game_folder1)-2];
			game_folder = game_folder1;

		from events import manager;
		if await_return:
			return manager.run(self, game_folder, game_file, game_arg, await_return);
		else:
			manager.run(self, game_folder, game_file, game_arg, await_return);

	def new_text(self, used_text="X"):
		check=True;
		gd = functions.get_gamedata();
	#	print(gd);
		try:
			exec("print(\""+gd["place"]+"\")");
		except:
			check=False;
		check2=True;
		gd = functions.get_gamedata();
	#	print(gd);
		try:
			exec("print(\""+str(gd["travel"])+"\")");
		except:
			check2=False;
		if check:
			place_functions.hub(self);
		else:
			if not hasattr(self, "alreadyruns"):
				self.alreadyruns = True;
			alreadyruns=False;
			if self.alreadyruns:
				alreadyruns=True;
				try:
					self.hub_time += 1;
					if self.hub_time == 3:
						self.hub_time = 0;
						self.game("hub", "system");
				except AttributeError:
					setattr(self, "hub_time", 0);
					pass;
				self.alreadyruns = False;
		#	print("HUB: "+str(self.hub_time))
			try:
				if check2 and not gd["travel"]["vehicle"]["events"]=="all":
					place_functions.hub(self, True);
				elif check2:
					if alreadyruns:
						gd["travel"]["steps"]-=1;
						functions.save_gamedata(gd);
						if gd["travel"]["steps"] <= 0:
							place_functions.hub(self, True);
			except KeyError:
				print("");
			else:
				alreadyused = functions.json_file_decode("user\\used_texts.json")[self.activemod];
				if used_text != "X":
					boo_i = False;
					for i in alreadyused:
						if alreadyused[i] == used_text:
							boo_i = True;
					if boo_i:
						game_folder1 = str(inspect.stack()[1][1])
						game_folder1 = game_folder1.split("\\");
						game_folder1 = game_folder1[len(game_folder1)-2];
						req = len(alreadyused[game_folder1])
						alreadyused[game_folder1][req]=used_text+".py";
						functions.json_file_encode("user\\used_texts.json", alreadyused);

				folders = [f.path for f in os.scandir("events") if f.is_dir() ]
				folder = [x[7:] for x in folders];
				random1 = {};
				file_count =0;
				for f in folder:
					if f != "__init__":
						if f!= "__pycache__":
							for file in os.scandir("events\\"+f):
								file = str(file)[11:-2];
								file_module = file[:-3];

								if file_module != "__init__":
									if file != "__pycache__":
										if f != "system":
											random1[str(file_count)]={"folder":f, "file":file_module}
											file_count += 1;
				print(random1);
				hg=random.random() * len(random1);
				self.game(random1[str(int(hg))]["file"], random1[str(int(hg))]["folder"]);


	#Valueable Functions
	def ending_game(self, event=None):
		self.root.quit();
		quit();

	#Usefull Functions hi
	def clear_screen(self):
		self.content_frame.forget();
		self.content_frame = Frame(self.root);
		self.content_frame.pack();

	def toggle_fullscreen(self, event=None):
		self.state = not self.state;
		self.root.attributes("-fullscreen", self.state);

	def hintergrund(self):
		return Canvas(self.content_frame, bg="Gold2", width=functions.pro_size(100,0), height=functions.pro_size(100,1), highlightthickness=0);

	def update(self):
		self.clear_screen();
		hintergrund1 = self.hintergrund();
		hintergrund1.pack();

		def run_updater():
			import update

		Label(hintergrund1, text="UPDATER LÄUFT", font=gui_content.ch_fontsize("32")).place(x=180, y=300);
		gui_content.button(hintergrund1, "Fertig!", 250, 350, self.main_menu, gui_content.ch_fontsize("20"));
		self.content_frame.after(0, run_updater);

		self.content_frame.mainloop();
