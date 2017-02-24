import os
from Lift_struct import *
from Message_Handling import encode_order, decode_order


#def truncate_and_write_my_orders_to_file(lift):
	#my_directory = os.getcwd()
#	file = open(my_directory + '/Orders.txt', 'w')

#	for i in range (0, len(lift.my_orders)):
#		file.write(encode_order(lift.my_orders[i]) + '\n')
#	file.close()

FILENAME = '/Orders.txt'

def append_to_file(order):
	my_directory = os.getcwd()
	file = open(my_directory + FILENAME, 'a')
	file.write(encode_order(order) + '\n')
	file.close()

def delete_order_from_file(order):
	my_directory = os.getcwd()
	file = open(my_directory + FILENAME, 'r')
	lines = file.readlines()
	file.close()

	file = open(my_directory + FILENAME, 'w')
	for line in lines:
		if ( line != encode_order(order) + '\n' and line != encode_order(order) ):
			file.write(line)
	file.close()

def read_order_list_from_file():
	my_directory = os.getcwd()
	file = open(my_directory + FILENAME, 'r')
	lines = file.readlines()
	file.close()

	order_list = []
	order_str = ''
	for line in lines:
		#decode_order(line)
		for i in range(0, len(line)):
			if(line[i] != '\n'):
				order_str = order_str + line[i]

		order_list.extend([decode_order(order_str)])
		order_str = ''

	file.close()

	return order_list