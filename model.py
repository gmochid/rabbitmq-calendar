import pika
import random
import re
import string

class Event(object):
	def __init__(self, name, place, start_date, end_date, information):
		self._name = name
		self._place = place
		self._start = start_date
		self._end = end_date
		self._information = information

	def __str__(self):
		return 'Name : %s\nPlace : %s\nStart Date : %s\nEnd Date : %s\nInformation : %s\n' % (self._name, 
			self._place, 
			self._start.strftime("%Y-%m-%d %H:%M:%S"), 
			self._end.strftime("%Y-%m-%d %H:%M:%S"), 
			self._information);

	# getter and setter name
	def get_nick(self):
		return self._name
	def set_nick(self, value):
		self._name = value
	def del_nick(self):
		del self._name
	name = property(get_nick, set_nick, del_nick, "Name Properties")

	# getter and setter place
	def get_place(self):
		return self._place
	def set_place(self, value):
		self._place = value
	def del_place(self):
		del self._place
	place = property(get_place, set_place, del_place, "Place Properties")

	# getter and setter start
	def get_start(self):
		return self._start
	def set_start(self, value):
		self._start = value
	def del_start(self):
		del self._start
	start = property(get_start, set_start, del_start, "Start Properties")

	# getter and setter end
	def get_end(self):
		return self._end
	def set_end(self, value):
		self._end = value
	def del_end(self):
		del self._end
	end = property(get_end, set_end, del_end, "End Properties")

	# getter and setter information
	def get_information(self):
		return self._information
	def set_information(self, value):
		self._information = value
	def del_information(self):
		del self._information
	information = property(get_information, set_information, del_information, "Information Properties")

class Calendar(object):
	def __init__(self, name):
		self._name = name
		self._events = []

	# getter and setter name
	def get_nick(self):
		return self._name
	def set_nick(self, value):
		self._name = value
	def del_nick(self):
		del self._name
	name = property(get_nick, set_nick, del_nick, "Name Properties")

	def print_calendar(self):
		for ev in self._events:
			print "Calendar : %s" % self._name
			print ev;

	def to_string(self):
		out_str = ""
		for ev in self._events:
			out_str += "Calendar : %s" % self._name
			out_str += "\n"
			out_str += ev.__str__()
			out_str += "\n"
		return out_str

	def get_events(self):
		return self._events

	def add_event(self,event):
		if isinstance(event, Event):
			self._events.append(event);

	def is_conflict(self, start_date, end_date):
		events = self._events
		for event in events:
			if (((end_date > event.start) and (start_date < event.start)) or
				((end_date > event.end) and (start_date < event.end)) or
				((end_date < event.end) and (start_date > event.start))):
				return True
		return False
