from Lift_struct import *

def add_order(order, orderlist):
	i = 0
	while (i < len(orderlist)): #Loop throws away duplicates
		if ((order.floor == orderlist[i].floor) and (order.direction == orderlist[i].direction)):
			i = 0
			break
		i = i + 1

	if (i == len(orderlist)):
		orderlist.extend([order])

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

def order_index_in_list(order, orderlist):
	value = -1
	for i in range (0, len(orderlist)):
		if (orders_are_equal(order, orderlist[i])):
			value = i
	if (value == -1):
		print("Order is not in list")
	return value
