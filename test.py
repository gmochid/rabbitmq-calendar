import thread
import time
import pika
import logging
import datetime
from helper import UserHelper
from model import Event, Calendar

cal = Calendar("MyCalendar")
ev = Event("Makan-makan", "D'Cost", datetime.datetime.now(), datetime.datetime.now(), "Yarwe")
ev2 = Event("Kuman", "Hupe", datetime.datetime.strptime("4 1 2014 15:58", "%d %m %Y %H:%M"), 
	datetime.datetime.strptime("6 1 2014 15:58", "%d %m %Y %H:%M"), "Gomul")
cal.add_event(ev)
cal.add_event(ev2)
x = datetime.datetime.strptime("4 1 2014 15:58", "%d %m %Y %H:%M")
z = x.strftime("%d:%m:%Y:%H:%M")
y = datetime.datetime.strptime(z, "%d:%m:%Y:%H:%M")
print y

print cal.is_conflict(
	datetime.datetime.strptime("5 1 2014 15:58", "%d %m %Y %H:%M"), 
	datetime.datetime.strptime("5 1 2014 15:58", "%d %m %Y %H:%M"))
