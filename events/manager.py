import os;
folders = [f.path for f in os.scandir("events") if f.is_dir() ]
folder = [x[7:] for x in folders];
random = [];
for f in folder:
	if f != "__init__":
		if f!= "__pycache__":
			try:
				os.remove(f+"\\__init__.py");
			except:
				pass
			all = "["
			for file in os.scandir("events\\"+f):
				file = str(file)[11:-2];
				file_module = file[:-3];

				if file_module != "__init__":
					if file != "__pycache__":
						all+="\""+file_module+"\",";
						
			all = all[:-1];
			all += "]";
			init_file = open("events\\"+f+"\__init__.py", "w");
			init_file.write("__all__ = "+all+";");
			init_file.close();
			
def run(gui, folder, game_file, game_arg="none", await_return=False):
	exec("from events."+folder+" import "+game_file);
	if game_arg != "none":
		if await_return:
			exec("return "+game_file+".init(gui, game_arg)");
		else:
			exec(game_file+".init(gui, game_arg)");
	else:
		if await_return:
			exec("return "+game_file+".init(gui)");
		else:
			exec(game_file+".init(gui)");
	gui.hook.onScreenReload.fire(gui.content_frame);