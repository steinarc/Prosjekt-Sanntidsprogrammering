from ctypes import *
import time
from threading import Thread
from Lift_struct import Lift 
from Lift_struct import Order


driver = CDLL("./../driver/libdriver.so")

def lift_init(lift):
	driver.elev_init()
	while(1):
		if (driver.elev_get_floor_sensor_signal() != -1):
			lift.floor = driver.elev_get_floor_sensor_signal()
		if (driver.elev_get_stop_signal() == 1):
			break
			
		



def lift_go(direction, lift):
	driver.elev_set_motor_direction(direction)
	lift.direction = direction	

def lift_stop(lift):
	lift_go(0, lift)


lift = Lift(2)

lift_thread = Thread(target = lift_init, args=(2))
lift_thread.start()
