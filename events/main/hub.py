from data import event_functions;
from data import functions;

class init():
	def __init__(self, gui):
		event_functions.textbox(self, gui, "Warten", [["**Weiter**", "hei"]]);
	def hei(self):
		self.gui.new_text();