from ctypes import *
import time
from threading import Thread
from Lift_struct import Lift 
from Lift_struct import Order


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
def listen_button(button_type, floor): #type: 0 = up, 1 = down, 2 = internal
	while(1):
		if (driver.elev_get_button_signal(button_type, floor) == 1):
			print("%d, i etasje %d" % (button_type, floor + 1))
			time.sleep(0.1)
		if (driver.elev_get_stop_signal() == 1): #Does not work right after
			driver.elev_set_stop_lamp(1)
			break



def listen_all_buttons(): #Run as thread
	thread1 = Thread(target = listen_button, args = (0,0))
	thread2 = Thread(target = listen_button, args = (0,1))
	thread3 = Thread(target = listen_button, args = (0,2))
	thread4 = Thread(target = listen_button, args = (1,1))
	thread5 = Thread(target = listen_button, args = (1,2))
	thread6 = Thread(target = listen_button, args = (1,3))
	thread7 = Thread(target = listen_button, args = (2,0))
	thread8 = Thread(target = listen_button, args = (2,1))
	thread9 = Thread(target = listen_button, args = (2,2))
	thread10 = Thread(target = listen_button, args = (2,3))
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



lift = Lift(2)
driver.elev_init()


#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN


#while(1):
#	time.sleep(0.1)

thread_lift = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
thread_lift.start()

lift_go(-1,lift)
time.sleep(3)
lift_stop(lift)
print(lift.floor)

thread_set_position = Thread(target = lift_go_to_floor, args = (2, lift, 0))
thread_set_position.start()


