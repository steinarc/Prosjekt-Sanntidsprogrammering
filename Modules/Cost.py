from Lift_struct import *

def my_cost(lift, order):
	return 0

def calculate_cost(lift, order):
	return 0

def find_lift_with_minimal_cost(lift):
	minimal = lift.costlist[lift.name]
	for i in range (0,3):
		if (lift.active_lifts[i] == 1):
			if (lift.costlist[i] < minimal and lift.costlist[i] != -1):
				minimal = lift.costlist[i]
				lift_name = i
	return lift_name



