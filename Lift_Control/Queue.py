from Lift_struct import Lift 
from Lift_struct import Order


def add_order(order, orderlist):
	orderlist.extend([order])

def print_order(order):
	print ("[%d, %d]" % (order.floor, order.direction))
	
def print_orderlist(orderlist):
	for i in range (0, len(orderlist)):
		print_order(orderlist[i])







