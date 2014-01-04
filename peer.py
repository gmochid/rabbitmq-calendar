import thread
import time
import pika
import logging
import datetime
from model import Event, Calendar
from helper import UserHelper, CalendarHelper

nickname_available = True
conflict = False
calendars = []
subscribers = []
user = UserHelper()
cal = CalendarHelper()



def user_callback(ch, method, properties, body):
	global nickname_available

	if body.split(' ')[0] == "[REGISTER]":
		if user.nickname != "":
			if user.nickname == body.split(' ')[1]:
				user.send_message(body="[RESPONSE] ERROR")
			else:
				user.send_message(body="[RESPONSE] OK")
	else:
		if user.nickname == "":
			if body.split(' ')[1] == "ERROR":
				nickname_available = False

def calendar_callback(ch, method, properties, body):
	if body.split(' ')[1] == user.nickname:
		if body.split(' ')[0] == "[SHOWEV]":
			calname = body.split(' ')[2]
			for calendar in calendars:
				if calname == calendar.name:
					cal.send_message(body="[SHOWEV_RES] %s %s"%(body.split(' ')[3], calendar.to_string()))
		elif body.split(' ')[0] == "[SHOWEV_RES]":
			temp = body.split(' ')[2:]
			disp = ' '.join(str(x) for x in temp)
			print disp
		elif body.split(' ')[0] == "[CHECK]":
			calname = body.split(' ')[2]
			start_date = datetime.datetime.strptime(body.split(' ')[4], "%d:%m:%Y:%H:%M")
			end_date = datetime.datetime.strptime(body.split(' ')[5], "%d:%m:%Y:%H:%M")

			for calendar in calendars:
				if calname == calendar.name:
					if calendar.is_conflict(start_date, end_date):
						cal.send_message(body="[CHECK_RES] %s ERROR" % body.split(' ')[3])

		elif body.split(' ')[0] == "[CHECK_RES]":
			if body.split(' ')[2] == "ERROR":
				conflict = True

def register_user():
	global nickname_available

	# setup connection
	user.bind_queue_exchange()
	user.register_listener(user_callback)
	thread.start_new_thread(user.start_consuming, ())
	
	while user.nickname == "":
		params = raw_input('Register username: ')
		nickname_available = True

		# send nick registration to all peer
		user.send_message(body="[REGISTER] %s" % params)
		
		# wait response for 5 seconds
		time.sleep(5)

		if nickname_available == True:
			user.nickname = params

	print "My username is %s" % (user.nickname)

if __name__ == '__main__':

	selected_calendar = None
	register_user()
	
	cal.bind_queue_exchange()
	cal.register_listener(calendar_callback)
	thread.start_new_thread(cal.start_consuming, ())

	print "Write HELP for complete command."

	params = raw_input('>> ')

	while params != "EXIT":
		if params == "ADDCAL":
			exist = True
			calname = ""

			# input calendar name
			while exist:
				calname = raw_input('Calendar Name: ')
				exist = False

				# check if there is existed calendar
				for calendar in calendars:
					if calendar.name == calname:
						exist = True
				if exist:
					print "Calendar with same name existed"

			# create calendar
			calendar = Calendar(calname)
			calendars.append(calendar)
			print "Calendar '%s' created" % (calname)

		elif params == "SELECTCAL":
			# check if exist calendar
			if len(calendars) == 0:
				print "There is no existing calendar"
			else:
				# input calendar name
				calname = raw_input('Calendar Name: ')

				# check if specified calendar exist
				exist = False
				for calendar in calendars:
					if calendar.name == calname:
						exist = True
						selected_calendar = calendar

				if exist:
					print "Calendar %s selected" % (calname)
				else:
					print "Calendar %s not exist" % (calname)

		elif params == "ADDEV":
			# check if there is selected calendar
			if selected_calendar == None:
				print "No selected calendar. Select calendar by SELECTCAL."
			else:
				# input information
				name = raw_input('Name: ')
				place = raw_input('Place: ')
				info = raw_input('Info: ')

				# input start date
				while True:
					try:
						start = raw_input('Start (DD MM YYYY HH:MM): ')
						start_date = datetime.datetime.strptime(start, "%d %m %Y %H:%M")
						break
					except ValueError:
						print "Format must be DD MM YYYY HH:MM"
				
				# input end date
				while True:
					try:
						end = raw_input('End (DD MM YYYY HH:MM): ')
						end_date = datetime.datetime.strptime(end, "%d %m %Y %H:%M")
						break
					except ValueError:
						print "Format must be DD MM YYYY HH:MM"

				# create event
				event = Event(name, place, start_date, end_date, info)
				selected_calendar.add_event(event)
				print "Event created"

		elif params == "SHOWEV":
			for calendar in calendars:
				calendar.print_calendar()

			for subs in subscribers:
				cal.send_message(body="[SHOWEV] %s %s %s" % (subs[0], subs[1], user.nickname))

			# wait response for 10 seconds
			time.sleep(5)

		elif params == "SUBSCRIBE":
			username = raw_input('Username: ')

			if username == user.nickname:
				print "Username cannot be self"
			else:
				calname = raw_input('Calendar Name: ')

				arr = []
				arr.append(username)
				arr.append(calname)

				subscribers.append(arr)
		elif params == "CHECK":
			conflict = False

			# input start date
			while True:
				try:
					start = raw_input('Start (DD MM YYYY HH:MM): ')
					start_date = datetime.datetime.strptime(start, "%d %m %Y %H:%M")
					break
				except ValueError:
					print "Format must be DD MM YYYY HH:MM"
			
			# input end date
			while True:
				try:
					end = raw_input('End (DD MM YYYY HH:MM): ')
					end_date = datetime.datetime.strptime(end, "%d %m %Y %H:%M")
					break
				except ValueError:
					print "Format must be DD MM YYYY HH:MM"

			for calendar in calendars:
				if calendar.is_conflict(start_date, end_date):
					conflict = True

			if conflict == False:
				for subs in subscribers:
					cal.send_message(body="[CHECK] %s %s %s %s %s" % 
						(subs[0], subs[1], user.nickname, start_date.strftime("%d:%m:%Y:%H:%M"), end_date.strftime("%d:%m:%Y:%H:%M")))

				# wait response for 5 seconds
				time.sleep(5)

			if conflict == True:
				print "Conflict happened"
			else:
				print "No conflict with other calendar"
		elif params == "HELP":
			print "ADDCAL"
			print "SELECTCAL"
			print "ADDEV"
			print "SHOWEV"
			print "SUBSCRIBE"
			print "CHECK"
		else:
			print "Undefined Command"

		params = raw_input('>> ')

	print "Bye :)"
	print "All Calendar and Event are destroyed"
