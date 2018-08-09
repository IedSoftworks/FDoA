import os;
import random
import tempfile
from tkinter import *;
from data import functions;
from data import gui_content;

def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False
	
class init():
	def __init__(self):
		self.root = Tk();
		self.root.geometry("900x800");
		self.root.title("Four Dragons of Apocalypse - Updater | IedSoftworks");
		self.hintergrund = Canvas(self.root, bg="blue", width=900, height=800);
		self.hintergrund.pack();

	def clear_screen(self):
		self.hintergrund.forget();
		self.hintergrund = Canvas(self.root, bg="blue", width=900, height=800);
		self.hintergrund.pack();

	def caracter_index(self):
		self.clear_screen();
		
		def install():
			self.root.quit();
			os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://iedsoftworks.com/server/fourdragonsofapocalypse/car_index.json', '%tmp%\\unversalcode.json')\"");
			g.config(text="Der Charakter-Index wird übernommen!");
			self.root.after(500, self.root.quit);
			self.root.mainloop();
			
			file_local = functions.json_file_decode("content/persons.json");
			file_server = functions.json_file_decode(tempfile.gettempdir()+"\\unversalcode.json");
			file_local = array_merge(file_local, file_server);
			for key, value in file_server.items():
				checkimg = True;
				try:
					print(value["img"]);
				except NameError:
					checkimg = False;
				except KeyError:
					checkimg = False;
				print(checkimg);
				
				if checkimg:
					print("Picture for "+key+" downloaded...");
					os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://iedsoftworks.com/server/fourdragonsofapocalypse/car_index_pics/"+file_server[key]["img"]+".gif', 'content\pictures\\"+file_server[key]["img"]+".gif')");
			functions.json_file_encode("content\persons.json", file_local);
			self.hintergrund.config(bg="green");
			g.config(text="Der Charakter-Index wurde übernommen und aktuellisert!", bg="green");
			self.root.after(3000, self.label);
			self.root.mainloop();
		
		g = Label(self.hintergrund, text="Der Charakter-Index wird runtergeladen!", font=gui_content.ch_fontsize("20"), fg="white", bg="blue");
		g.place(x=200, y=300);
		
		g.after(500, install);
		self.root.mainloop();

	def event(self):
		list = [];
		for file in os.scandir("events"):
			file = str(file)[11:-2];
			list.append(file);
		list.remove("__init__.py");
		list.remove("__pycache__");
		
		os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://iedsoftworks.com/server/fourdragonsofapocalypse/get_events.php', '%tmp%\\7456.txt')");
		file_server = functions.json_file_decode(tempfile.gettempdir()+"\\7456.txt");
		file_server = file_server["list"];
		
		file_local = list;
		downloadedfiles = [];
		
		for value in file_server:
			check = True;
			for value1 in file_local:
				if value == value1:
					check = False;
			if check:
				print(value);
				downloadedfiles.append(value);
		print(downloadedfiles);
		
		if len(downloadedfiles) != 0:
			key = str(random.randint(100000000000, 999999999999));
			for value in downloadedfiles:
				print(value);
				os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://iedsoftworks.com/server/fourdragonsofapocalypse/event_actions.php?a=copy&file="+value+"&key="+key+"', '%tmp%\fiuoh')");
			os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://iedsoftworks.com/server/fourdragonsofapocalypse/event_actions.php?a=zipper&key="+key+"', '%tmp%\\aiff.tmp')");
			#os.system("powershell -command \"start-bitstransfer -source http://iedsoftworks.com/server/fourdragonsofapocalypse/event_tmp/event_files_"+key+".zip -destination %tmp%\\update.zip\"");

			
	def all(self):
		print("all");	
	
	def ping(self):
		self.clear_screen();
		x=Message(self.hintergrund, font=gui_content.ch_fontsize("16"), text="VERBINDUNG ZUM STANDART-SERVER\nWIRD ÜBERPRÜFT!\n(iedsoftworks.com)", width=500, bg="blue", fg="white").place(x=200, y=200);
		self.root.after(100, self.root.quit);
		self.root.mainloop();
		check_server = os.system("ping iedsoftworks.com");
		if check_server != 0:
			x.config(text="ALLGEMEINE INTERNETVERBINDUNG\nWIRD GETESTET!\n(google.com)");
			self.root.after(100, self.root.quit);
			self.root.mainloop();
			check_net = os.system("ping google.com");
			if check_net != 0:
				x.config(text="Es scheint, du hättest keine Internetverbindung. Bitte verbinde dein PC mit dem Internet oder schalte die Firewall für dieses Programm frei.");
				Button(self.hintergrund, command=self.end,text="Updater beenden", bd=8, bg="navy").place(x=300, y=600, width=100, height=100);
				self.root.mainloop();
			self.std_server = False;
		if check_server == 0:
			self.std_server = True;
		self.select_server();
		
	def select_server(self):
		self.clear_screen();
		self.getback = Label(self.hintergrund, text="Server-Auswahl", font=gui_content.ch_fontsize("20"), bg="blue", fg="white");
		self.getback.place(x=375, y=100);
		
		def standart():
			self.net = "iedsoftworks.net";
			self.label();
		
		if not self.std_server:
			Label(self.hintergrund, text="Standart-Server nicht erreicht", font=gui_content.ch_fontsize("13"), bg="blue", fg="white").place(x=200, y=200);
		else:
			Button(self.hintergrund, text="Standart-Server", command=standart, font=gui_content.ch_fontsize("14"), bd=8, bg="green").place(x=200, y=200);
		
		custom_server_frame = Frame(self.hintergrund, bg="blue");
		Label(custom_server_frame, text="Custom Server / Mods", bg="blue", fg="white", font=gui_content.ch_fontsize("16")).pack();
		custom_server_frame.place(x=500,y=170);
		self.custom_server_input = Entry(custom_server_frame, font=gui_content.ch_fontsize("13"))
		self.custom_server_input.pack();
		Button(custom_server_frame, text="Übernehmen", command=self.custom_server, bd=8, font=gui_content.ch_fontsize("16"),bg="green").pack();
		self.root.mainloop();
		
	def custom_server(self):
		server = self.custom_server_input.get();
		self.getback.config(text="Server wird angepingt...");
		serverping = os.system("ping "+server);
		if serverping != 0:
			self.getback.config(text="Server hat nicht geantwortet");
			self.root.mainloop();
		else:
			serverinstall = os.system("powershell -Command \"(New-Object Net.WebClient).DownloadFile('http://"+server+"/server/fourdragonsofapocalypse/installed.php', '%tmp%\\60205.txt')");
			if serverinstall != 0:
				self.getback.config(text="Server wurde nicht installiert...");
				self.root.mainloop();
			else:
				self.net = server;
				self.label();
			
	def label(self):
		self.clear_screen();
		frame = Frame(self.hintergrund, bg="blue");
		Label(frame, text="Aktueller Server: "+self.net, font=gui_content.ch_fontsize("15"), bg="blue", fg="white").pack();
		Button(frame, text="Ändern", command=self.select_server, font=gui_content.ch_fontsize("12"), bg="green").pack();
		frame.place(x=10, y=10);
		
		Label(self.hintergrund, text="Was möchtest du updaten?", font=gui_content.ch_fontsize("16"),bg="blue", fg="white").place(x=375, y=250);
		gui_content.button(self.hintergrund, "Charakter-Index", 400, 350, self.caracter_index, gui_content.ch_fontsize("16"), ["green", "black"], [150, 50]);
		Button(self.hintergrund, text="Events", command=self.event, font=gui_content.ch_fontsize("16"), bg="green", bd=8).place(x=400, y=420, width=150, height=50);
		gui_content.button(self.hintergrund, "Alles", 400, 490, self.all, gui_content.ch_fontsize("16"), ["green", "black"], [150, 50]);
		self.root.mainloop();

gui = init();
gui.ping();		
