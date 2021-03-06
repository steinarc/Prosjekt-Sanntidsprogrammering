from Lift_struct import *

#Interface functions

def calculate_cost(lift, order):
	return (len(lift.my_orders) + abs(lift.floor - order.floor))

def find_lift_with_minimal_cost(lift):
	minimal = lift.costlist[lift.name]
	lift_name = lift.name
	for i in range (0,3):
		if (lift.active_lifts[i] == 1):
			if (lift.costlist[i] < minimal and lift.costlist[i] != -1):
				minimal = lift.costlist[i]
				lift_name = i
	return lift_name

def costlist_is_full(lift):
	truth = True
	for i in range (0,3):
		if(lift.costlist[i] == -1 and lift.active_lifts[i] == 1):
			truth = False
	return truth

