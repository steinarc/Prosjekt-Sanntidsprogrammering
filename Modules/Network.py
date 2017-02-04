import socket
import select
import time
import Queue
from Lift_struct import *
from Queue_module import *
from threading import Thread

def find_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])

def UDP_send(ip, port, data):
	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_send.sendto(data, (ip, port))
	

def UDP_receive(port, timeout, return_queue):
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.bind(('', port)) #maa bruke egen IP her
	sock_receive.setblocking(0)	
	data = '0'

	ready = select.select([sock_receive], [], [], timeout)
	if (ready[0]):
		data, addr = sock_receive.recvfrom(1024)
	if(data == '0'):
		print("nothing was received")	

	return_queue.put(data)
	return data

def UDP_send_and_spam_until_confirmation(remote_ip, port, data):
	confirmation = '0'

	return_queue = Queue.Queue() #Use queue to get the return value of the thread
	confirmation_thread = Thread(target = UDP_receive, args = (port+1, 4, return_queue)) # 4 second timeout
	confirmation_thread.start()

	while(confirmation_thread.isAlive()): #While we wait for a confirmation send over and over again
		UDP_send(remote_ip, port, data)
		time.sleep(0.1)
	
	confirmation = return_queue.get()	

	if (confirmation == '0'):
		print ("My friend has died")
	else:
		print("Message sent and my friend is still alive")


def UDP_receive_and_confirm(ip, port, timeout):
	remote_ip = ip
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.bind((ip, port))
	sock_receive.setblocking(0)	
	data = '0'	

	ready = select.select([sock_receive], [], [], timeout)
	if (ready[0]):
		data, addr = sock_receive.recvfrom(1024)
		UDP_send(remote_ip, port+1, '1')
	return (data)
		







#Message handling

def encode_order(Order):
	return ("%d %d" %(Order.floor, Order.direction))

def decode_order(message):
	if (message[0].isdigit() == False):	
		print("Message is invalid")
		return Order(0,0) #0,0-order is invalid order and will do nothing
	floor = int(message[0])
	if (message[2] == '-'):
		if (message[3].isdigit() == False):	
			print("Message is invalid")
			return Order(0,0)
		direction = int(message[2:4])
	else:
		if (message[2].isdigit() == False):	
			print("Message is invalid")
			return Order(0,0)
		direction = int(message[2])

	return Order(floor, direction)


# A message is for ex: "0,Order,3 -1,11"

def classify_and_decode_message(message_string):
	if (message_string != '0'):
		message = message_string.split(',')
		if (message[1] == 'Order'):
			decode_order_message(message)
		elif(message[1] == "Alive"):
			decode_Im_alive_message(message)
	else:
		print("No message to decode")


def encode_order_message(lift, order):
	s1 = ("%d," %(lift.name))
	s2 = "Order,"
	s3 = ("%d %d," % (order.floor, order.direction))
	s4 = "0" #cost
	return s1 + s2 + s3 + s4

def decode_order_message(message): #message is a list
	lift_name = int(message[0])
	order = decode_order(message[2])
	cost = int(message[3])
	print_order(order)

def encode_Im_alive_message(lift):
	s1 = ("%d," %(lift.name))
	s2 = "Alive,"
	s3 = ("%d," %(lift.is_alive))
	return s1 + s2 + s3

def decode_Im_alive_message(message): #message is a list
	
	return 0