from data import gui;
import pdb
from data import pyevent;
from pathlib import Path
from data import getgui;
import os;
import sys;

args = sys.argv;
args.pop(0);

#pdb.set_trace();

f = True;
try:
	args[0];
except IndexError:
	f = False;
if f:
	if args[0] == "-mod":
		mod = args[1];
	else:
		mod = "main";
else:
	mod = "main";

gui1 = gui.GUI();
gui1.hook = pyevent.Hook(gui1);
# All Events contain the gui object as "gui" arg.
gui1.hook.addevent("onInit"); #

gui1.hook.addevent("onScreenReload"); # Background-Canvas
gui1.hook.addevent("onTextbox"); # Text, Buttons

gui1.hook.addevent("onEventInit"); # Dir, Event, Args
gui1.hook.addevent("onEventEnd"); #

gui1.hook.addevent("onFightInit"); # Fight Object
gui1.hook.addevent("onFightEnd"); # Fight Object, Outcome: 0 - Won; 1 - Escaped; 2 - Lost
gui1.hook.addevent("onFightAttackEnemy"); # Fight Object, Weapon, Target Enemy ID.
gui1.hook.addevent("onFightAttackAlli"); # Fight Object, Weapon, Target Player Name.

gui1.hook.addevent("onPlaceRegister"); # Place data
gui1.hook.addevent("onPlaceEnter"); # Place name
gui1.hook.addevent("onPlaceLeave"); # Place name

gui1.hook.addevent("onContainerRegister"); # Container ID
gui1.hook.addevent("onContainerOpen"); # Container ID, Container Data.
gui1.hook.addevent("onContainerMoveToCon"); # Container ID, Container Data, Player Inventory, Moved Item, Amount, Return Event, Return Function
gui1.hook.addevent("onContainerMoveToInv"); # Container ID, Container Data, Player Inventory, Moved Item, Amount, Return Event, Return Function

gui1.hook.addevent("onFactionRegister"); # Faction Data
gui1.hook.addevent("onFactionValue"); # Faction Data, Given Value, Calculated Value

gui1.hook.addevent("onItemAdd"); # Item, Amount
gui1.hook.addevent("onItemRemove"); # Item, Amount
gui1.hook.addevent("onItemCheck"); # Item
gui1.hook.addevent("onItemAction"); # Item, Event, Event Folder.
for f in os.scandir("mods"):
	if f.is_dir():
		init = Path(f.path+"/init.py");
		if init.exists():
			exec("from mods."+f.name+" import init");
			exec("init.init(gui1)");
gui1.hook.onInit.fire();
getgui.gui(gui1);
gui1.system_start(mod);