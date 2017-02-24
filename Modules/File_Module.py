import os
from Lift_struct import *
from Message_Handling import encode_order


#def truncate_and_write_my_orders_to_file(lift):
	#my_directory = os.getcwd()
#	file = open(my_directory + '/Orders.txt', 'w')

#	for i in range (0, len(lift.my_orders)):
#		file.write(encode_order(lift.my_orders[i]) + '\n')
#	file.close()

def append_to_file(order):
	my_directory = os.getcwd()
	file = open(my_directory + '/Orders.txt', 'a')
	file.write(encode_order(order) + '\n')
	file.close()

def delete_order_from_file(order):
	my_directory = os.getcwd()
	file = open(my_directory + '/Orders.txt', 'r')
	lines = file.readlines()
	file.close()	

	file = open(my_directory + '/Orders.txt', 'w')
	for line in lines:
		if ( line != encode_order(order) + '\n'):
			file.write(line)


