import time
from threading import Thread, Lock
from Lift_struct import *
from Queue_module import *
from driver import *


def lift_find_floor(lift):
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

def lift_go_to_floor(floor, lift, timeout):
	prev_floor = -1
	while(1):
		if (driver.elev_get_stop_signal() == 1):
			lift_stop(lift)
			break

		if (prev_floor != lift.floor):
			if (lift.floor == floor):
				lift_stop(lift)
				break
			elif (lift.floor < floor):
				lift_go(1,lift)
			else:
				lift_go(-1,lift)
			prev_floor = lift.floor




#This function prints if ONLY ONE selected button is pressed

def execute_order(lift):
	if (len(lift.my_orders) > 0):
		lift_go_to_floor(lift.my_orders[0].floor, lift, 0)
		lift.my_orders.pop(0)


#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN

lift = Lift(0)
driver.elev_init()


thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,))
thread_lift_find_floor.start()
thread_listen_buttons.start()


while(1):
	execute_order(lift)



