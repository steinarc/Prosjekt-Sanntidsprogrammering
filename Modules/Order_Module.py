from Lift_struct import *
from File_Module import append_to_file
from Lock_Manager import lock

#interface functions

def add_order_external_list(lift, order):
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
	pos = len(orderlist) - 1
	while (i < len(orderlist)): #Loop throws away duplicates
		if ((order.floor == orderlist[i].floor) and (order.direction == orderlist[i].direction)):
			i = 0
			break
		i = i + 1

	direction = 0;
	if (i == len(orderlist)): #Add the order, sort list

		if (order.direction == 0):
			append_to_file(order)
			with lock:
				lift.my_orders.extend([order])
		else:
			with lock:
				lift.my_orders.extend([order])





#		if (order.direction == 0): #order.direction == 0 means internal order all orders in my_orders will have a direction!!
#			if (order.floor < lift.floor): #Hvis vi maa ned for aa gjoere ordren
#				for x in range (0,len(orderlist)):
#					if (orderlist[x].direction == -1):
#						pos = x
#						while (orderlist[pos].direction == -1 and orderlist[pos].floor > order.floor):
#							pos += 1
#						break
#
#			elif (order.floor > lift.floor): #Hvis vi maa opp for aa gjoere ordren
#				for x in range (0,len(orderlist)):
#					if (orderlist[x].direction == 1):
#						pos = x
#						while (orderlist[pos].direction == 1 and orderlist[pos].floor < order.floor):
#							pos += 1
#						break

#		lift.my_orders.insert(pos,Order(order.floor, ))


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

