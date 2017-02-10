from Lift_struct import *


# A message is for ex: "0,Order,3 -1"
# A message is for ex: "0,Alive"
# A message is for ex: "0,Cost,11"

def send_order_message(lift, order):
	message = encode_order_message(lift,order)
	for i in range (0,3):
		if (i != lift.name and lift.active_lifts[i] == 1):
			remote_ip = lift.ip_list[i]
			send_and_spam_until_confirmation(remote_ip, PORT, message)




def classify_message(message_string):
	if (message_string != '0'):
		message = message_string.split(',')
		if (message[1] == 'Alive' or message[1] == 'Order' or message[1] == 'Cost' or message[1] == 'Command' or message[1] == 'Executed'):
			return message[1]
		else:
			print("Invalid message")
			return '0'
	else:
		print("No message to decode")



def encode_order_message(lift, order):
	s1 = ("%d," %(lift.name))
	s2 = "Order,"
	s3 = ("%d %d," % (order.floor, order.direction))
	s4 = "0" #cost
	return s1 + s2 + s3 + s4

def decode_order_message(message): #message is a string
	message = message.split(',')
	lift_name = int(message[0])
	order = decode_order(message[2])
	return lift_name, order #Will return other values as well

def encode_Im_alive_message(lift):
	s1 = ("%d," %(lift.name))
	s2 = "Alive,"
	s3 = ("%d," %(lift.is_alive))
	return s1 + s2 + s3

def decode_Im_alive_message(message):
	message = message.split(',')
	lift_name = int(message[0])
	alive = int(message[2])
	return lift_name, alive

def encode_command_message(lift, order):
	s1 = ("%d," % (lift.name))
	s2 = "Command,"
	s3 = encode_order(order)
	return s1 + s2 + s3

def decode_command_message(message):
	message = message.split(',')
	lift_name = int(message[0])
	order = decode_order(message[2])
	return lift_name, order

def encode_cost_message(lift, order):
	s1 = ("%d," % (lift.name))
	s2 = "Cost,"
	s3 = encode_order(order)
	s4 = (",%d" % (calculate_cost(lift,order)))
	return s1 + s2 + s3 + s4

def decode_cost_message(message):
	message = message.split(',')
	lift_name = int(message[0])
	order = decode_order(message[2])
	cost = int(message[3])
	return lift_name, order, cost

def encode_executed_message(lift, order):
	s1 = ("%d," % (lift.name))
	s2 = "Executed,"
	s3 = encode_order(order)
	return s1 + s2 + s3

def decode_executed_message(message): #So put your hands down my pants and i bet youll feel nuts
	message = message.split(',')
	lift_name = int(message[0])
	order = decode_order(message[2])
	return lift_name, order


def encode_order(order): #Returns a string
	return ("%d %d" %(order.floor, order.direction))

def decode_order(message): #Returns an order object from a string
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
