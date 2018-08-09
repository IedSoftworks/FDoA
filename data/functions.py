import ctypes;
import os;
import ast;
import json;
from tkinter import *;


def get_screensize(m):
	return int(ctypes.windll.user32.GetSystemMetrics(m))

def file_to_dict(file):
	return str_to_dict(read_file_content(file));

def str_to_dict(str):
	settings = ast.literal_eval(str);
	return settings

def pro_size(pro, pos):
	# 0 = Weite
	# 1 = Höhe
	screen = int(ctypes.windll.user32.GetSystemMetrics(pos));
	screen = screen / 100;
	screen = screen * pro;
	return int(screen);
	
def pause(visual = False):
	if (visual):
		pause_tmp = lambda: os.system("pause");
	else:
		pause_tmp = lambda: os.system("pause>nul");
	pause_tmp();

def cls():
	cls = lambda: os.system("cls");
	cls();

def put_content_in_file(file, content):
	open(file, "w").write(content);

def read_file_content(file, delfile = False, deln = False):
	file_content = open(file, "r").read();
	if delfile:
		os.remove(file);
	if deln:
		return file_content.replace("\n", "");
	return file_content;

def exist_variable(var):
	exec("print("+var+")");
	try:
		exec("print("+var+")");
	except NameError:
		return False;
	except KeyError:
		return False;
	return True;

def json_file_decode(file):
	return json_str_decode(read_file_content(file));

def json_str_decode(str):
	return json.loads(str);

def json_file_encode(file, content):
	put_content_in_file(file, json_str_encode(content));

def json_str_encode(content):
	return json.dumps(content);

def run_edit_file(modulestr):
	x = lambda: os.system("start \"\" \"..\\system\\Notepad++Portable\\Notepad++Portable.exe\" \"addons\\"+modulestr+".py\"");
	x();

def os_put_file_content(file, content):
	osx = lambda: os.system("echo "+content+">>"+file);
	osx();

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():

                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

def get_gamedata():
	return json_file_decode("user\gamedata.json");
	
def save_gamedata(array):
	json_file_encode("user\gamedata.json", array);
	
def get_persons_content():
	return json_file_decode("content\persons.json");

def get_inventory():
	try:
		return get_gamedata()["inventory"];
	except:
		return {};
def save_inventory(array):
	add_json_string("user\gamedata.json", "inventory", array);
def add_json_string(file, key, value):
	try:
		file1 = json_file_decode(file);
	except:
		file1 = {};
	file1[key] = value;
	json_file_encode(file, file1);

def get_json_file(file, key = "none", ifs = False):
	file1 = json_file_decode(file);
	if key == "none":
		return file1;
	else:
		if ifs:
			varexist = True;
			try:
				file1[key];
			except NameError:
				varexist = False;
			except KeyError:
				varexist = False;
		
			if varexist:
				return True;
			else:
				return False;
		else:
			return file1[key];

def del_json_value(file, key):
	file1 = json_file_decode(file);
	del file1[key];
	json_file_encode(file, file1);