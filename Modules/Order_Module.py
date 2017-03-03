from Lift_struct import *
from File_Module import append_to_file
from Lock_Manager import lock

#interface functions

def add_order_to_all_external_orders(lift, order):
	i = 0
	while (i < len(lift.all_external_orders)): #Loop throws away duplicates
		if ((order.floor == lift.all_external_orders[i].floor) and (order.direction == lift.all_external_orders[i].direction)):
			i = 0
			break
		i = i + 1

	direction = 0;
	if (i == len(lift.all_external_orders)):
		with lock:
			lift.all_external_orders.extend([order])

def add_order_to_my_orders(lift,order):
	orderlist = lift.my_orders
	i = 0
	direction = order.direction
	if (direction == 0):
		append_to_file(Order(order.floor, direction))

	while (i < len(orderlist)): #Loop throws away duplicates
		if ((order.floor == orderlist[i].floor) and (order.direction == orderlist[i].direction)
			or ( (order.direction == 0) and (order.floor == orderlist[i].direction))):
			i = 0
			break
		i = i + 1

	if (i == len(orderlist)): #Add the order, sort list

		if (direction == 0):
			if (lift.floor > order.floor):
				direction = -1
			else:
				direction = 1
			
		with lock:
			lift.my_orders.extend([order])




def order_index_in_list(order, orderlist):
	value = -1
	for i in range (0, len(orderlist)):
		if (orders_are_equal(order, orderlist[i])):
			value = i
	if (value == -1):
		print("Order is not in list")
	return value


#Addtitional functions


def print_order(order):
	print ("[%d, %d]" % (order.floor, order.direction))
	
def print_orderlist(orderlist):
	for i in range (0, len(orderlist)):
		print_order(orderlist[i])

def orders_are_equal(order1, order2):
	if ((order1.floor == order2.floor) and (order1.direction == order2.direction)):
		return True
	else:
		return False

