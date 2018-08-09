from data import event_functions;

class init():
	def __init__(self, gui, arg):
		self.gui = gui
		event_functions.textbox(self, arg[0]+" wartet... und wartet... und wartet... und wartet... und wartet... und wartet...", [["Das tut er!!", "test", "navy"], ["STOP!!!", "test1", "navy"], ["STOP!!!", "test", "navy"]]);
	def test(self):
		self.gui.new_text("startgame");
	def test1(self):
		self.gui.game("test");