from data import functions;
from data import gui_content
from functools import partial
from collections import defaultdict
from tkinter import *;
from tkinter import font;
import random;
import time;


def caracter_manager(gui, car, mode, arg="none"):
	if mode == "check_use_caracter":
		x_bool = False;
		for x in functions.get_gamedata()["caracters"]:
			if functions.get_gamedata()["caracters"][x] == car:
				x_bool=True;

		if x_bool:
			return True;
		else:
			return False;
	elif mode == "set_caracter":
		gamedata = functions.get_gamedata();
		check = True;
		if len(gamedata["caracters"]) >= 4:
			result = gui.game("fullteam", [car], True);
			check = result[0];
			gamedata = result[1];
		if check:
			gamedata["caracters"].append(car);
			print(str(gamedata));
		functions.save_gamedata(gamedata);
	elif mode == "get_car_data":
		persons = functions.get_persons_content();
		return persons[car.fight_caracter];
	elif mode == "get_car_data_tmp":
		persons = car.content["tmpfriends"];
		return persons[car.fight_caracter];
	elif mode == "givedisc":
		json = functions.json_file_decode("user\\found_description.json");
		json.append(car);
		functions.json_file_encode("user\\found_description.json");

def get_group(mode):
	return list(functions.get_gamedata()["caracters"].keys());
def randomize(value, if_value = False):
	value1 = random.random() * 1000000;
	if value1 < value:
		if if_value:
			return [True, value1]
		else:
			return True;
	else:
		if if_value:
			return [False, value1];
		else:
			return False;

def add_items(items):
	inv = functions.get_inventory();
	from data.getgui import gui;
	for item, amount in items.items():
		test = True
		try:
			inv[item]
		except NameError:
			test = False;
		except KeyError:
			test = False;
		except IndexError:
			test = False;
		gui.hook.onItemAdd.fire(item, amount);
		if test:
			inv[item] += amount;
		else:
			inv[item] = amount;

	functions.save_inventory(inv);

def check_item(item):
	from data.getgui import gui;
	inv = functions.get_inventory();
	try:
		amount = inv[item];
	except:
		amount = 0;
	gui.hook.onItemCheck.fire(item);
	return amount;

def remove_items(item, amount):
	from data.getgui import gui;
	inv = functions.get_inventory();
	inv[item] -= amount
	if inv[item] < 0:
		inv[item] =0;
	gui.hook.onItemRemove.fire(item, amount);
	functions.save_inventory(inv);

# Important functions
def trade(classi, gui, trading):
	# trading syntax: {"ITEM":"AMOUNT=COINS"}
	class init():
		def __init__(self):
			self.boolean = True;

	selfi = init();
	if not gui:
		gui = classi.gui;
	gui.clear_screen();
	classi.gui = gui;
	hintergrund1 = gui.hintergrund();
	hintergrund1.pack();

	shoppinglist1 = Canvas(hintergrund1, width=functions.pro_size(80,0), height=functions.pro_size(60,1), bg="green")
	shoppinglist1.place(x=functions.pro_size(10,0), y=functions.pro_size(15,1), anchor=NW);
	shoppinglist = functions.VerticalScrolledFrame(shoppinglist1);
	shoppinglist.place(width=functions.pro_size(80,0), height=functions.pro_size(60,1));

	def buy(item, value, selfi):
		coins = functions.get_gamedata()["inventory"]["coins"];
		value1 = int(int(coins) / int(value));

		buyer = Canvas(hintergrund1, width=functions.pro_size(40,0), height=functions.pro_size(7.5,1))
		buyer.place(x=functions.pro_size(50,0), anchor=N, y=functions.pro_size(3.75,1));
		itembanner = Label(hintergrund1, text=item, font=gui_content.ch_fontsize("16"), bg="gold2")
		itembanner.place(x=functions.pro_size(50,0), y=functions.pro_size(1,1), anchor=N);
		buyer1 = Frame(buyer);
		buyer1.place(x=0, y=0);
		Label(buyer1, text="Du kaufst ").grid(column=1, row=1)
		entry = functions.NumericEntry(buyer1);

		def cal_value(*args):
			if entry.result.get() == 0:
				buy.config(text="Kaufen (0)");
			else:
				value1 = entry.result.get() * int(value);
				buy.config(text="Kaufen ("+str(value1)+")")

		def buy1():
			value1 = entry.result.get() * int(value);
			Label(buyer1, text="Möchtest wirklich das kaufen?").grid(column=3, row=1, columnspan=2);

			def yes():
				remove_items("coins", value1);
				add_items({item:entry.result.get()});
				no();

			def no():
				buyer.place_forget();
				buyer.destroy();
				itembanner.place_forget();
				itembanner.destroy();

			Button(buyer1, text="Ja", command=yes).grid(column=3, row=2);
			Button(buyer1, text="Nein", command=no).grid(column=4, row=2);

		buy = Button(buyer1, text="Kaufen ("+value+")", command=buy1);
		buy.grid(column=1, row=2, columnspan=2);
		entry.result.trace("w", cal_value);
		entry.frame.grid(column=2, row=1);

	xrow = 0;
	for item, value in trading.items():
		xrow += 1
		setattr(selfi, "trader_canvas"+str(xrow), Canvas(shoppinglist.interior, width=functions.pro_size(79,0), height=functions.pro_size(10,1), bg="green"))
		getattr(selfi, "trader_canvas"+str(xrow)).grid(row = xrow)
		Label(getattr(selfi, "trader_canvas"+str(xrow)), text=item, font=gui_content.ch_fontsize("30"), bg="green", fg="white").place(x=functions.pro_size(5,0), y=functions.pro_size(5,1), anchor=W)
		Label(getattr(selfi, "trader_canvas"+str(xrow)), text=value+" Geld", bg="green", fg="white").place(x=functions.pro_size(39.5,0), y=functions.pro_size(9.5,1), anchor=S)
		Button(getattr(selfi, "trader_canvas"+str(xrow)), text="Kaufen?", command=partial(buy, item, value, selfi)).place(x=functions.pro_size(79,0), y=functions.pro_size(5,1), anchor=E);
def textbox(classi, text, button):
	classi.gui.alreadyruns = True;
	classi.gui.clear_screen();
	hintergrund1 = classi.gui.hintergrund();

	hintergrund1.pack();
	
	classi.gui.hook.onTextbox.fire(text, button);
	
	textbox = Canvas(hintergrund1, height=functions.pro_size(40,1), width=functions.pro_size(80,0), bg="Gold2",highlightthickness=0);
	textbox.place(x=functions.pro_size(10,0), y=functions.pro_size(5,1));
	Message(textbox, text=text, font=gui_content.ch_fontsize("14"), width=functions.pro_size(78,0), bg="Gold2").place(x=functions.pro_size(2,0));

	buttonbox = Canvas(hintergrund1, height=functions.pro_size(30,1), width=functions.pro_size(50,0), bg="Gold2")
	buttonbox.place(x=functions.pro_size(50,0), y=functions.pro_size(80,1), anchor=CENTER);
	columnx = 0;
	rowx = 1;
	for x in button:
		columnx += 1;
		if columnx == 3:
			rowx +=1;
			columnx=1;

		try:
			x[2];
		except IndexError:
			x.append("navy");

		exec("Button(buttonbox, text=\""+x[0]+"\", command=classi."+x[1]+", bg=\""+x[2]+"\", width=functions.pro_size(4,0), height=functions.pro_size(0.6,1), font=gui_content.ch_fontsize(\"16\"), fg=\"white\").grid(row=rowx, column=columnx)");
	classi.gui.hook.onScreenReload.fire(hintergrund1);
def fight_screen(classi, content):
	class selfi():
		def __init__(self):
			self.true = True;

	self = selfi();
	self.gui = classi.gui;
	self.gui.alreadyruns = True;
	self.gui.clear_screen();
	self.classi = classi;
	hintergrund1 = self.gui.hintergrund();
	hintergrund1.pack();
	self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
	self.commands.place(y=functions.pro_size(80,1));
	self.main_screen = Canvas(hintergrund1, bg="yellow", width=860, height=550);
	self.main_screen.place(x=20, y=30);
	
	self.content = content;

	self.fight = {};
	self.fight["alli"] = {};
	self.fight["enemys"] = {};

	allis = Canvas(self.main_screen, bd=0, bg="yellow",width=400, height=500, highlightthickness=0)
	allis.place(x=15, y=50);
	Label(self.main_screen, text="Team", font=gui_content.ch_fontsize("20"),bg="yellow").place(x=20, y=10);
	self.banner = Label(hintergrund1, text="Kampf gestartet...", bg="gold2",font=gui_content.ch_fontsize("16"));
	self.banner.place(x=450, anchor=N);

	rowx = 0
	self.allilist={};
	for caracter, content in functions.get_gamedata()["caracters"].items():
		rowx +=1;
		setattr(self, "alli"+str(rowx)+"selectedc", Canvas(allis, width=20, height=20, bg="yellow", highlightthickness=0));
		setattr(self, "alli"+str(rowx)+"selectedcircle", getattr(self, "alli"+str(rowx)+"selectedc").create_oval(1, 1, 20, 20, fill="red", outline="yellow"));
		getattr(self, "alli"+str(rowx)+"selectedc").grid(column=1, row = rowx);
		setattr(self, "alli"+str(rowx)+"name", Label(allis, bg="yellow", text=caracter, font=gui_content.ch_fontsize("14")))
		getattr(self, "alli"+str(rowx)+"name").grid(column=2, row = rowx);
		setattr(self, "alli"+str(rowx)+"hp", Label(allis, bg="yellow", text="HP: "+str(content["hp"]), font=gui_content.ch_fontsize("14")));
		getattr(self, "alli"+str(rowx)+"hp").grid(column=3, row = rowx);
		self.fight["alli"][str(rowx)]={"hp":content["hp"], "name":caracter, "tmp":False};
	if "tmpfriends" in self.content:
		for caracter, content in self.content["tmpfriends"].items():
			rowx +=1;
			setattr(self, "alli"+str(rowx)+"selectedc", Canvas(allis, width=20, height=20, bg="yellow", highlightthickness=0));
			setattr(self, "alli"+str(rowx)+"selectedcircle", getattr(self, "alli"+str(rowx)+"selectedc").create_oval(1, 1, 20, 20, fill="red", outline="yellow"));
			getattr(self, "alli"+str(rowx)+"selectedc").grid(column=1, row = rowx);
			setattr(self, "alli"+str(rowx)+"name", Label(allis, bg="yellow", text=caracter, font=gui_content.ch_fontsize("14")))
			getattr(self, "alli"+str(rowx)+"name").grid(column=2, row = rowx);
			setattr(self, "alli"+str(rowx)+"hp", Label(allis, bg="yellow", text="HP: "+str(content["hp"]), font=gui_content.ch_fontsize("14")));
			getattr(self, "alli"+str(rowx)+"hp").grid(column=3, row = rowx);
			self.fight["alli"][str(rowx)]={"hp":content["hp"], "name":caracter, "tmp":True};

	Label(self.main_screen, text="Enemys", font=gui_content.ch_fontsize("20"),bg="yellow").place(x=450, y=10);
	self.enemyscreen = Canvas(self.main_screen, bd=0, bg="yellow",width=400, height=500, highlightthickness=0)
	self.enemyscreen.place(x=445, y=50);
	rows = 0;
	self.enemylist = {};
	for name, value in self.content["enemys"].items():
		try:
			value["multi"];
		except:
			value["multi"] = 1;
		for x in range(value["multi"]):
			x +=1;
			rows += 1;
			setattr(self, "enemys"+str(rows)+"name", Label(self.enemyscreen, bg="yellow", text=name, font=font.Font(family=('MS', 'Sans', 'Serif'), size=14)));
			getattr(self, "enemys"+str(rows)+"name").grid(column=1, row=rows);
			setattr(self, "enemys"+str(rows)+"hp", Label(self.enemyscreen, font=gui_content.ch_fontsize("14"),bg="yellow", text="HP: "+str(value["hp"])));
			getattr(self, "enemys"+str(rows)+"hp").grid(column=2, row=rows);
			self.fight["enemys"][str(rows)]={"hp":value["hp"], "name":name, "attacks":value["attacks"]}

	def create_attack_list(self, modi, id, value):
		if modi== "add":
			if len(self.attacklist) < value["target"]:
				self.attacklist.append(id);

		title = "";
		for ids in self.attacklist:
			title += self.fight["enemys"][str(ids)]["name"]+",";
		title = title[:-1];
		self.banner.config(text="Kampf: Wähle "+str(value["target"])+" Gegner: "+title);
		if len(self.attacklist) == value["target"]:
			self.banner.config(text="Kampf: "+str(value["target"])+" ausgewählt.");
			attack2(self, value);

	def ai(self):
		id = random.choice(list(self.fight["enemys"].keys()));
		attack = random.choice(list(self.fight["enemys"][str(id)]["attacks"].keys()));
		dmg = str(self.fight["enemys"][str(id)]["attacks"][str(attack)]["dmg"]);
		if "chance" in self.fight["enemys"][str(id)]["attacks"][str(attack)]:
			chance=self.fight["enemys"][str(id)]["attacks"][str(attack)]["chance"];
		else:
			chance=100;
		target = random.choice(list(self.fight["alli"].keys()));

		self.banner.config(text="Kampf: "+self.fight["enemys"][id]["name"]+" trifft "+self.fight["alli"][str(target)]["name"]+" mit "+attack+". "+str(dmg)+" Schaden");
		make_dmg(self, target, {"dmg":int(dmg), "chance":chance}, "alli");

	def make_dmg(self, id, value, mode):
		if mode == "alli":
			self.gui.hook.onFightAttackAlli.fire(self, value, id);
		else:
			self.gui.hook.onFightAttackEnemy.fire(self, value, id);
		applydmg=True;
		if "chance" in value:
			rvalue = int(random.randint(1,100));
			if rvalue > int(value["chance"]):
				applydmg=False;
				self.banner.config(text="Fehlschuss.");
		if applydmg:
			self.fight[mode][str(id)]["hp"] -= value["dmg"];
		car_menu = False;
		if self.fight[mode][str(id)]["hp"]<= 0:
			self.fight[mode][str(id)]["hp"] = 0;
			getattr(self, mode+str(id)+"name").config(fg="red", font=font.Font(family=('MS', 'Sans', 'Serif'), size=14, overstrike=1));
			getattr(self, mode+str(id)+"hp").config(text="HP: "+str(self.fight[mode][str(id)]["hp"]),fg="red", font=font.Font(family=('MS', 'Sans', 'Serif'), size=14, overstrike=1) );
			if self.fight_caracter == self.fight[mode][str(id)]["name"]:
				print("if workxs")
				car_menu = True;
			self.fight[mode].pop(str(id));
			if car_menu:
				select_caracters_menus(self);
		else:
			getattr(self, mode+str(id)+"hp").config(text="HP: "+str(self.fight[mode][str(id)]["hp"]));

	def attack(self, attack, value):
		if value["target"]!="all":
			self.attacklist = [];
			self.banner.config(text="Kampf: Wähle "+str(value["target"])+" Gegner:");
			for id in self.fight["enemys"]:
				setattr(self, "enemys"+str(id)+"attackbutton",Button(self.enemyscreen, bg="yellow", text="Angriff", font=gui_content.ch_fontsize("14"), command=partial(create_attack_list, self, "add",id, value)));
				getattr(self, "enemys"+str(id)+"attackbutton").grid(column=3, row=id);
		else:
			attack2(self, value);

	def attack2(self, value):
		for id in self.fight["enemys"]:
			getattr(self, "enemys"+str(id)+"attackbutton").grid_forget();

		if value["target"]!= "all":
			for id in self.attacklist:
				make_dmg(self, id, value, "enemys");
		else:
			for id in self.fight["enemys"]:
				make_dmg(self, id, value, "enemys");

		def ai_start():
			ai(self);
			actions_phase(self);

		if len(self.fight["enemys"]) == 0:
			self.commands.forget();
			self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
			self.commands.place(y=functions.pro_size(80,1));
			self.gui.hook.onFightEnd(self, 0);
			exec("Button(self.commands, text=\"Gewonnen.\", font=gui_content.ch_fontsize(\"16\"), command=self.classi."+self.content["win"]["func"]+").place(y=functions.pro_size(10,1), x=functions.pro_size(50,0), anchor=CENTER)")
		else:
			def waitmsg():
				self.banner.config(text="Bitte warten...")
			self.banner.after(1500, waitmsg);
			self.commands.forget();
			self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
			self.commands.place(y=functions.pro_size(80,1));
			self.banner.after(4500, ai_start);

	def actions_phase(self):
		self.commands.forget();
		self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
		self.commands.place(y=functions.pro_size(80,1));

		attacklist = Canvas(self.commands, bg="white");
		attacklist.place(y=functions.pro_size(1.5,1), x=functions.pro_size(37,0), width=functions.pro_size(60,0), height=functions.pro_size(18,1));

		rowg = 0;
		mode = "get_car_data";
		if self.fight_caracter_data["tmp"]:
			mode = "get_car_data_tmp";
		for attacks, dmg in caracter_manager(self.gui, self, mode)["attacks"].items():
			rowg += 1;
			Button(attacklist, relief=FLAT, bg="white",text=" - "+attacks, command=partial(attack, self, attacks, dmg), font=gui_content.ch_fontsize("15")).grid(row=rowg, sticky=W);

		Button(self.commands, text="Kämpfer ändern", font=gui_content.ch_fontsize("16"), command=partial(select_caracters_menus, self)).place(x=functions.pro_size(5,0), y=functions.pro_size(5,1));

	def run(self):
		self.commands.forget();
		self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
		self.commands.place(y=functions.pro_size(80,1));
		chance = self.content["runaway"]["chance"];
		rand_value = random.random() * 100;
		print(rand_value);
		if rand_value < chance:
			self.gui.hook.onFightEnd(1, self);
			exec("Button(self.commands, text=\"Erfolgreich.\", font=gui_content.ch_fontsize(\"16\"), command=self.classi."+self.content["runaway"]["func"]+").place(y=functions.pro_size(10,1), x=functions.pro_size(50,0), anchor=CENTER)");
		else:
			def ai_start():
				ai(self);

			self.fight_caracter = self.fight["alli"]["1"]["name"];
			self.fight_caracter_id = "1";

			self.banner.config(text="Flucht fehlgeschlagen...");
			self.banner.after(2000, ai_start);

	def select_caracters_menus(self):
		self.commands.forget();
		self.commands = Canvas(hintergrund1, bg="brown", width=functions.pro_size(100,0), height=functions.pro_size(20,1));
		self.commands.place(y=functions.pro_size(80,1));

		def selectcaracter(caracter, id, self):
			self.fight_caracter = caracter["name"];
			self.fight_caracter_data = caracter;
			self.fight_caracter_id = id;
			for carid in range(len(self.fight["alli"])):
				carid += 1;
				getattr(self, "alli"+str(carid)+"selectedc").itemconfig(getattr(self, "alli"+str(carid)+"selectedcircle"),fill="red");
			getattr(self, "alli"+str(id)+"selectedc").itemconfig(getattr(self, "alli"+str(id)+"selectedcircle"),fill="green");
			actions_phase(self);
		if len(self.fight["alli"]) != 0:
			caracters = Canvas(self.commands, bg="red", width=functions.pro_size(75,0), height=functions.pro_size(15,1));
			columnx=0;
			rowx=0;
			id =0;
			for key, value in self.fight["alli"].items():
				columnx += 1;
				if columnx == 3:
					rowx +=1;
					columnx=1;
				Button(caracters, text=value["name"], width=functions.pro_size(3, 0), height=functions.pro_size(0.5,1), command=partial(selectcaracter, value, key, self)).grid(column=columnx, row=rowx);

			caracters.place(x=functions.pro_size(50,0),y=functions.pro_size(10,1), anchor=CENTER);

			Button(self.commands, text="Fliehen", command=partial(run, self), font=gui_content.ch_fontsize("16")).place(x=5,y=5);

		else:
			Label(self.main_screen, text="VERLOREN",font=gui_content.ch_fontsize("50")).place(x=50, y=50, anchor=NW);
			self.gui.hook.onFightEnd(self, 0);
			
	self.gui.hook.onFightInit.fire(self);
	select_caracters_menus(self);
def register_itemaction(data):
	from data.getgui import gui;
	if not hasattr(gui, "itemevents"):
		setattr(gui, "itemevents", {});
	if not data["item"] in gui.itemevents:
		gui.itemevents[data["item"]] = {};
	gui.itemevents[data["item"]][data["name"]]=data["event"];
def adddoc(name, file):
	register_itemaction({"item":"Dokumente","name":"Öffnen","event":["system","book"]});
	add_items({"Dokumente":1});
	gd = functions.get_gamedata();
	if not "unlockeddocs" in gd:
		gd["unlockeddocs"]={};
	gd["unlockeddocs"][name]=file;
	functions.save_gamedata(gd);