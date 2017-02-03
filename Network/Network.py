import socket
import select
import time
from Orderstruct import *

def find_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])

def UDP_send(ip, port, data):
	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_send.sendto(data, (ip, port))
	

def UDP_receive(ip, port, timeout):
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.bind((ip, port))
	sock_receive.setblocking(0)	
	data = -1	

	ready = select.select([sock_receive], [], [], timeout)
	if (ready[0]):
		data, addr = sock_receive.recvfrom(1024)
	if(data == -1):
		print("UDP_receive() timed out")	
	return (data)

def UDP_receive_and_confirm(ip, port, timeout):
	remote_ip = ip
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.bind((ip, port))
	sock_receive.setblocking(0)	
	data = 0	

	ready = select.select([sock_receive], [], [], timeout)
	if (ready[0]):
		data, addr = sock_receive.recvfrom(1024)
		UDP_send(remote_ip, port+1, "OK")
		UDP_send(remote_ip, port+1, "OK")# 3 times to make sure
		UDP_send(remote_ip, port+1, "OK")# the message is received
	return (data)
		

def UDP_send_and_spam_until_confirmation(ip, port, data, max_attempts):
	my_ip = ip
	attempts = 0
	response = 0
	while(response == 0):
		UDP_send(ip, port, data)
		response = UDP_receive(my_ip, port+1, 1)
		attempts += 1
		if (attempts >= max_attempts):
			print("No connection") # Other elevator is dead
			break


def encode_order_message(Order):
	return ("%d %d" %(Order.floor, Order.direction))


def decode_order_message(message):
	if (message[0].isdigit() == False):	
		print("Message is invalid")
		return Order(0,0) #0,0-order is invalid order
	floor = int(message[0])
	if (message[2] == '-'):
		direction = int(message[2:4])
	else:
		direction = int(message[2])

	return Order(floor, direction)


# A message is for ex: "0, New Order, 3 -1, 11 "





