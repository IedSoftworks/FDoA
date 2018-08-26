import pickle

class AdvancedFight():
	def __init__(self):
		self.tools = {};
		self.characters = {};
	def regtool(self, name="Tool", space="main", usage=0, blockareas=[], energy=0, RemOnUsageErr=False, applyeffects=[]):
		name = space+"."+name;
		self.tools[name]=AFObject();
		self.tools[name].name=name;
		self.tools[name].effects=applyeffects;
		self.tools[name].cooldown=cooldown;
		self.tools[name].usage=usage;
		return self.tools[name];
	def regcharacter(self, name="Character", space="main", energy=100, hp=100, effects=[]):
		name = space+"."+name;
		self.characters[name]=AFObject();
		self.characters[name].name=name;
		
	def getByName(self, type, name, space="main"):
		name = space+"."+name;
		try:
			exec("return self."+type+"s["+name+"];");
		except KeyError, AttributeError:
			return AFObject();
			
class AFObject():
	def __init__(self):
		pass;