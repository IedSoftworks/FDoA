from data import event_functions;
from data import functions;

class init():
	def __init__(self, gui, arg=[]):
		self.gui = gui;
		event_functions.add_items({"Test-Item":5});
		event_functions.textbox(self, "Item-Test", [["get", "get", "navy"], ["delete", "del1", "navy"], ["STOP!!!", "exit", "navy"]]);
		
	def get(self):
		print(event_functions.check_item("Test-Item"));
		
	def del1(self):
		event_functions.remove_items("Test-Item", 2);
	
	def exit(self):
		self.gui.new_text("inv");