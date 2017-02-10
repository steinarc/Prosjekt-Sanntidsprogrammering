from ctypes import *
from threading import Thread
from Lift_struct import *
from Lift_Control import *

driver = CDLL("./../driver/libdriver.so")

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

def lift_find_floor(lift):
	while(1):
		floor = driver.elev_get_floor_sensor_signal()
		if (floor != -1):
			lift.floor = floor
			driver.elev_set_floor_indicator(lift.floor)

		if (driver.elev_get_stop_signal() == 1):
			break

def lift_move_direction(lift, direction):
	driver.elev_set_motor_direction(direction)
	lift.direction = direction	

def lift_stop(lift):
	lift_move_direction(lift, 0)