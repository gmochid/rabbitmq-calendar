import pika
import random
import re
import string

VOWEL = 'aiueo'
CONSONANT = 'bcdfghjklmnpqrstvwxyz'

class UserHelper(object):
	exchange_list = []

	def __init__(self, host="localhost"):
		self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
		self._channel = self._connection.channel()
		self._id = '107-%s' % self.get_random_nick()
		self._nickname = ""

		self.register_queue()


	# getter and setter connection
	def get_conn(self):
		return self._connection
	def set_conn(self, value):
		self._connection = value
	def del_conn(self):
		del self._connection
	connection = property(get_conn, set_conn, del_conn, "Connection Properties")

	# getter and setter channel
	def get_ch(self):
		return self._channel
	def set_ch(self, value):
		self._channel = value
	def del_ch(self):
		del self._channel
	channel = property(get_ch, set_ch, del_ch, "Channel Properties")

	# getter and setter id
	def get_id(self):
		return self._id
	def set_id(self, value):
		self._id = value
	def del_id(self):
		del self._id
	id = property(get_id, set_id, del_id, "ID Properties")

	# getter and setter nickname
	def get_nick(self):
		return self._nickname
	def set_nick(self, value):
		self._nickname = value
	def del_nick(self):
		del self._nickname
	nickname = property(get_nick, set_nick, del_nick, "Nickname Properties")

	def register_exchange(self, exchange_name='user'):
		self._channel.exchange_declare(exchange='107-%s' % exchange_name, type='fanout')

	def register_queue(self):
		self._channel.queue_declare(self._id)

	def register_listener(self, callback, no_ack=True):
		self._channel.basic_consume(callback, queue=self._id, no_ack=no_ack)

	def bind_queue_exchange(self, exchange_name='user'):
		self.register_exchange(exchange_name)
		self._channel.queue_bind(exchange='107-%s' % exchange_name, queue=self._id)
		UserHelper.exchange_list.append(exchange_name)

	def unbind_queue_exchange(self, exchange_name='user'):
		self._channel.queue_unbind(exchange='107-%s' % exchange_name, queue=self._id)
		UserHelper.exchange_list.remove(exchange_name)

	def publish_message(self, body='Hello World!!'):
		for exchange in UserHelper.exchange_list:
			self.send_message(exchange_name=exchange, body=body)

	def send_message(self, exchange_name='user', body='Hello World!!'):
		self._channel.basic_publish(exchange='107-%s' % exchange_name, routing_key='', body='%s' % (body))

	def start_consuming(self):
		self._channel.start_consuming()

	def close_connection(self):
		self._connection.close()

	def get_random_nick(self):
		nick = ''
		for i in range(random.randint(6, 10)):
			nick += VOWEL[random.randint(0, len(VOWEL) - 1)]
			nick += CONSONANT[random.randint(0, len(CONSONANT) - 1)]
		return nick

class CalendarHelper(object):
	exchange_list = []

	def __init__(self, host="localhost"):
		self._connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
		self._channel = self._connection.channel()
		self._id = '107-%s' % self.get_random_nick()
		self._nickname = ""

		self.register_queue()


	# getter and setter connection
	def get_conn(self):
		return self._connection
	def set_conn(self, value):
		self._connection = value
	def del_conn(self):
		del self._connection
	connection = property(get_conn, set_conn, del_conn, "Connection Properties")

	# getter and setter channel
	def get_ch(self):
		return self._channel
	def set_ch(self, value):
		self._channel = value
	def del_ch(self):
		del self._channel
	channel = property(get_ch, set_ch, del_ch, "Channel Properties")

	# getter and setter id
	def get_id(self):
		return self._id
	def set_id(self, value):
		self._id = value
	def del_id(self):
		del self._id
	id = property(get_id, set_id, del_id, "ID Properties")

	# getter and setter nickname
	def get_nick(self):
		return self._nickname
	def set_nick(self, value):
		self._nickname = value
	def del_nick(self):
		del self._nickname
	nickname = property(get_nick, set_nick, del_nick, "Nickname Properties")

	def register_exchange(self, exchange_name='calendar'):
		self._channel.exchange_declare(exchange='107-%s' % exchange_name, type='fanout')

	def register_queue(self):
		self._channel.queue_declare(self._id)

	def register_listener(self, callback, no_ack=True):
		self._channel.basic_consume(callback, queue=self._id, no_ack=no_ack)

	def bind_queue_exchange(self, exchange_name='calendar'):
		self.register_exchange(exchange_name)
		self._channel.queue_bind(exchange='107-%s' % exchange_name, queue=self._id)
		CalendarHelper.exchange_list.append(exchange_name)

	def unbind_queue_exchange(self, exchange_name='calendar'):
		self._channel.queue_unbind(exchange='107-%s' % exchange_name, queue=self._id)
		CalendarHelper.exchange_list.remove(exchange_name)

	def publish_message(self, body='Hello World!!'):
		for exchange in CalendarHelper.exchange_list:
			self.send_message(exchange_name=exchange, body=body)

	def send_message(self, exchange_name='calendar', body='Hello World!!'):
		self._channel.basic_publish(exchange='107-%s' % exchange_name, routing_key='', body='%s' % (body))

	def start_consuming(self):
		self._channel.start_consuming()

	def close_connection(self):
		self._connection.close()

	def get_random_nick(self):
		nick = ''
		for i in range(random.randint(6, 10)):
			nick += VOWEL[random.randint(0, len(VOWEL) - 1)]
			nick += CONSONANT[random.randint(0, len(CONSONANT) - 1)]
		return nick
