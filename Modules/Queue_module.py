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
