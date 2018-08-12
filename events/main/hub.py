from data import event_functions;
from data import functions;

class init():
	def __init__(self, gui):
		self.gui = gui;
		event_functions.textbox(self, "Warten", [["**Weiter**", "hei"]]);
	def hei(self):
		self.gui.new_text();