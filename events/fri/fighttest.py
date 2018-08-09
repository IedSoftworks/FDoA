from data import event_functions;
from data import functions;

class init():
	def __init__(self, gui):
		self.gui = gui;
		event_functions.textbox(self, "Ein Raider greift dich an!", [["Los gehts!", "start"]]);
	
	def start(self):
		event_functions.fight_screen(self, {"enemys":{"Raider":{"hp":16, "multi":2, "attacks":{"Pistole":{"dmg":1}, "Sturmgewehr":{"dmg":1}}}, "RadScorp":{"hp":64, "attacks":{"Stachel":{"dmg":1}, "Hit":{"dmg":1}}}},"runaway":{"chance":99, "func":"hallo"},"win":{"func":"hallo"}});
	
	def hallo(self):
		print("Hallo");