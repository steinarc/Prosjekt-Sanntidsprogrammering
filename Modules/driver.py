from ctypes import *
import time
from threading import Thread
from Lift_struct import *
from Lock_Manager import lock

driver = CDLL("./../driver/libdriver.so")


#Interface functions

def listen_all_buttons(lift, internal_button_queue, external_button_queue): #Run as thread
	thread1 = Thread(target = listen_button, args = (0,0,lift, internal_button_queue, external_button_queue))
	thread2 = Thread(target = listen_button, args = (0,1,lift, internal_button_queue, external_button_queue))
	thread3 = Thread(target = listen_button, args = (0,2,lift, internal_button_queue, external_button_queue))
	thread4 = Thread(target = listen_button, args = (1,1,lift, internal_button_queue, external_button_queue))
	thread5 = Thread(target = listen_button, args = (1,2,lift, internal_button_queue, external_button_queue))
	thread6 = Thread(target = listen_button, args = (1,3,lift, internal_button_queue, external_button_queue))
	thread7 = Thread(target = listen_button, args = (2,0,lift, internal_button_queue, external_button_queue))
	thread8 = Thread(target = listen_button, args = (2,1,lift, internal_button_queue, external_button_queue))
	thread9 = Thread(target = listen_button, args = (2,2,lift, internal_button_queue, external_button_queue))
	thread10 = Thread(target = listen_button, args = (2,3,lift, internal_button_queue, external_button_queue))
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
			with lock:
				lift.floor = floor
			driver.elev_set_floor_indicator(lift.floor)

		if (driver.elev_get_stop_signal() == 1):
			driver.elev_set_stop_lamp(1)
			with lock:
				lift.stopped = 1
			break

def lift_move_direction(lift, direction):
	driver.elev_set_motor_direction(direction)
	if (direction != 0):
		with lock:
			lift.direction = direction	

def lift_stop(lift):
	lift_move_direction(lift, 0)


def set_external_lamp(order, value):
	button = 0
	if (order.direction == 1):
		button = 0
	elif (order.direction == -1):
		button = 1
	driver.elev_set_button_lamp(button, order.floor, value)

def set_internal_lamp(order, value):
	button = 2
	driver.elev_set_button_lamp(button, order.floor, value)

#Additional functions

def listen_button(button_type, floor, lift, internal_button_queue, external_button_queue): #type: 0 = up, 1 = down, 2 = internal
	direction = 0
	while(1):
		if (driver.elev_get_button_signal(button_type, floor) == 1):		
			if (button_type == 2):
				order = Order(floor, 0) #direction = 0 for internal order
				with lock:
					internal_button_queue.put(order)
				set_internal_lamp(order, 1)
			else:
				if (button_type == 0):
					direction = 1
				elif (button_type == 1):
					direction = -1
				order = Order(floor, direction)
				with lock:
					external_button_queue.put(order)			
			time.sleep(1)
		if (lift.stopped == 1): #Does not work right after
			break