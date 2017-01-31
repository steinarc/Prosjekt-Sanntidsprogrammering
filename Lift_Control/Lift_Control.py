from ctypes import *
import time
from Lift_struct import Lift

mylib = CDLL("./../driver_py/libdriver.so")

def lift_go(lift, direction):
	mylib.elev_set_motor_direction(direction)
	lift.direction = direction	

def lift_stop(lift):
	lift_go(lift, 0)

def detect_floor(lift):
	lift_go(lift,-1)
	while (1):
		if (mylib.elev_get_floor_sensor_signal() != -1):
			a = mylib.elev_get_floor_sensor_signal()
			lift_stop(lift)
			lift.floor = a
			return a

def go_to_floor(floor, lift): # Både denne og detect er møkkajalla
	while (lift.floor != floor):
		if (lift.floor < floor):
			lift_go(lift, 1)
		elif (lift.floor > floor):
			lift_go(lift,-1)
		else:
			print("Framme!")
			lift.stop(lift)

frode = Lift(2)

mylib.elev_init()
detect_floor(frode)
go_to_floor(1,frode)

