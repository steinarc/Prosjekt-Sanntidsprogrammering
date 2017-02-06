from ctypes import *
import time
from threading import Thread, Lock
from Lift_struct import *
from Queue_module import *


driver = CDLL("./../driver/libdriver.so")

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
def listen_button(button_type, floor, lift): #type: 0 = up, 1 = down, 2 = internal
	direction = 0
	while(1):
		if (driver.elev_get_button_signal(button_type, floor) == 1):
			#print("%d, i etasje %d" % (button_type, floor + 1))			
			if (button_type == 2):
				order = Order(floor, 0) #direction = 0 for internal order

				add_order(order, lift.my_orders)
			else:
				if (button_type == 0):
					direction = 1
				elif (button_type == 1):
					direction = -1
				order = Order(floor, direction)
				add_order(order, lift.all_external_orders)
			time.sleep(0.1)
		if (driver.elev_get_stop_signal() == 1): #Does not work right after
			driver.elev_set_stop_lamp(1)
			break



def listen_all_buttons(lift): #Run as thread
	thread1 = Thread(target = listen_button, args = (0,0,lift))
	thread2 = Thread(target = listen_button, args = (0,1,lift))
	thread3 = Thread(target = listen_button, args = (0,2,lift))
	thread4 = Thread(target = listen_button, args = (1,1,lift))
	thread5 = Thread(target = listen_button, args = (1,2,lift))
	thread6 = Thread(target = listen_button, args = (1,3,lift))
	thread7 = Thread(target = listen_button, args = (2,0,lift))
	thread8 = Thread(target = listen_button, args = (2,1,lift))
	thread9 = Thread(target = listen_button, args = (2,2,lift))
	thread10 = Thread(target = listen_button, args = (2,3,lift))
	thread1.start()
	thread2.start()
	thread3.start()
	thread4.start()
	thread5.start()
	thread6.start()
	thread7.start()
	thread8.start()
	thread9.start()
	thread10.start()

def execute_order(lift):
	if (len(lift.my_orders) > 0):
		lift_go_to_floor(lift.my_orders[0].floor, lift, 0)
		lift.my_orders.pop(0)


lift = Lift(2)
driver.elev_init()

#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN


#while(1):
#	time.sleep(0.1)

thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,))
thread_lift_find_floor.start()
thread_listen_buttons.start()


order = Order(1,1)




