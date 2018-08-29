class EventHook(object):

	def __init__(self, gui):
		self.__handlers = []
		self.gui=gui;

	def register(self, handler):
		self.__handlers.append(handler)
		return self

	def remove(self, handler):
		self.__handlers.remove(handler)
		return self

	def fire(self, *args, **keywargs):
		for handler in self.__handlers:
			keywargs["gui"]=self.gui;
			handler(*args, **keywargs)

	def clearHandlers(self, inObject):
		for theHandler in self.__handlers:
			if theHandler.im_self == inObject:
				self -= theHandler
class Hook():
	def __init__(self, gui):
		self.gui=gui;
	def addevent(self, name):
		setattr(self, name, EventHook(self.gui));
	def removehook(self, name):
		delattr(self, name);
	def clearHandlers(self, name):
		getattr(self, name, EventHook()).clearHandlers();
	def fire(self, name, *args, **keywargs):
		getattr(self, name, EventHook()).fire(*args, **keywargs);