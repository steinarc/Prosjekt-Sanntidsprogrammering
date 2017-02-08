import time
from threading import Thread, Lock
from Lift_struct import *
from Queue_module import *
from driver import *
from Message_Handling import *
from Network import *

driver = CDLL("./../driver/libdriver.so")

def lift_find_floor(lift):
	while(1):
		if (driver.elev_get_floor_sensor_signal() != -1):
			lift.floor = driver.elev_get_floor_sensor_signal()
		if (driver.elev_get_stop_signal() == 1):
			break

def lift_move_direction(lift, direction):
	driver.elev_set_motor_direction(direction)
	lift.direction = direction	

def lift_stop(lift):
	lift_move_direction(lift, 0)

def lift_go_to_floor(lift, floor, timeout):
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
				lift_move_direction(lift, 1)
			else:
				lift_move_direction(lift, -1)
			prev_floor = lift.floor


def execute_order(lift):
	if (len(lift.my_orders) > 0):
		lift_go_to_floor(lift, lift.my_orders[0].floor, 0)
		lift.my_orders.pop(0)


#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN


def send_order_active_lifts(lift, order):	
	message = encode_order_message(lift,order)
	for i in range (0,3):
		if (i != lift.name and lift.active_lifts[i] == 1):
			remote_ip = lift.ip_list[i]
			send_and_spam_until_confirmation(remote_ip, PORT, message)

def receive_message_and_act(lift, port): #will always be run as a thread ALWAYS!
	while(1):
		message = receive_and_confirm(lift, port) # The function will wait here until something is received
		message_type = classify_message(message)

		if (message_type == 'Order'):
			lift_name, order = decode_order_message(message)
		#Calculate my cost
		#send it back to the sender in a cost-message


		elif(message_type == 'Alive'):
			lift_name, alive = decode_Im_alive_message(message)
			lift.active_lifts[lift_name] = alive
		elif(message_type == 'Cost'):
			return 0
		elif(message_type == 'Command'):
				lift_name, order = decode_command_message(message)
				add_order(order, lift.my_orders)
		elif(message_type == 'Executed'):
			return 0


	# Ta hensyn til hvilken type melding dette er.
	#hvis dette er en ordremelding. regn ut cost og send tilbake din cost
	#Hvis dette er en im alive-melding sett Is_alive
	#Hvis dette er en Cost-melding legg til i costlist
	#Hvis dette er en 

