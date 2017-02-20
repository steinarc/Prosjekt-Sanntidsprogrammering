import time
from threading import Thread, Lock
from Lift_struct import *
from Queue_module import *
from driver import *
from Message_Handling import *
from Network import *

driver = CDLL("./../driver/libdriver.so")

def lift_go_to_floor(lift, floor, timeout):
	prev_floor = -1
	while(1):
		if (lift.stopped == 1):
			lift_stop(lift)
			break

		if (prev_floor != lift.floor):
			if (lift.floor == floor):
				lift_stop(lift)
				driver.elev_set_door_open_lamp(1)
				time.sleep(2)
				driver.elev_set_door_open_lamp(0)
				break
			elif (lift.floor < floor):
				lift_move_direction(lift, 1)
			else:
				lift_move_direction(lift, -1)
			prev_floor = lift.floor


def execute_order(lift):
	if (len(lift.my_orders) > 0):
		lift_go_to_floor(lift, lift.my_orders[0].floor, 0)
		if (lift.floor == lift.my_orders[0].floor and lift.direction == lift.order[0].direction):
			send_executed_message(lift,order)
			set_external_lamp(lift.my_orders[0],0)
			with lock:
				lift.my_orders.pop(0)


#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN

def listen_external_buttons_and_send_order(lift,port,button_queue):
	while(1):
		if (lift.stopped == 1): #Does not work right after
			break
		if (button_queue.empty() == 0):
			order = button_queue.get()
			with lock:
				add_order(order, lift.all_external_orders)
				lift.costlist[lift.name] = calculate_cost(lift,order)
			send_order_message(lift,order)



		

def receive_message(lift, port, received_messages_queue): #will always be run as a thread ALWAYS!
	while(1):
		message = receive_and_confirm(lift, port) # The function will wait here until something is received
		with lock:
			received_messages_queue.put(message)



def respond_to_message(lift,received_messages_queue):
	while(1):
		if (received_messages_queue.empty() == 0):

			message = received_messages_queue.get()
			message_type = classify_message(message)

			if (message_type == 'Order'):
				print("Order message received")
				sending_lift, order = decode_order_message(message)
				cost = calculate_cost(lift, order)
				send_cost_message(lift, order, sending_lift)
		
			elif(message_type == 'Alive'):
				print("Alive message received")
				lift_name, alive = decode_Im_alive_message(message)
				with lock:
					lift.active_lifts[lift_name] = alive
		
			elif(message_type == 'Cost'):
				print("Cost message received")
				lift_name, order, cost = decode_cost_message(message)
				print(message)
				#with lock:
				lift.costlist[lift_name] = cost	 ##Do this for both elevators!!!!
				if (costlist_is_full(lift)):
					lift_with_minimal_cost_name = find_lift_with_minimal_cost(lift)
					if (lift_with_minimal_cost_name == lift.name):
						with lock:
							add_order(order, lift.my_orders)
					else:
						send_command_message(lift, order, lift_with_minimal_cost_name)
					set_external_lamp(order, 1)	
					lift.costlist = [-1, -1, -1]

				#add costs to lift.costlist, when list i full, find least cost and
				#Then send_command_message
			elif(message_type == 'Command'):
				print("Command message received")
				lift_name, order = decode_command_message(message)
				with lock:
					add_order(order, lift.my_orders)
			elif(message_type == 'Executed'):
				lift_name, order = decode_executed_message(message)
				set_external_lamp(order, 0)
				index = order_index_in_list(order, lift.all_external_orders)
				if (index > 0):
					with lock:
						lift.all_external_orders.pop(index)
					print("Order successfully removed")
				

#driver.elev_set_floor_indicator(3), viser hvor vi er.
#driver.elev_set_button_lamp(button, floor, value), button: 0 = OPP, 1 = NED, 2 = HEISPANEL, value = AV/PA, 0/1
#driver.elev_set_door_open_lamp(0) #, DOR APEN

def set_external_lamp(order, value):
	button = 0
	if (order.direction == 1):
		button = 0
	elif (order.direction == -1):
		button = 1
	driver.elev_set_button_lamp(button, order.floor, value)

	# Ta hensyn til hvilken type melding dette er.
	#hvis dette er en ordremelding. regn ut cost og send tilbake din cost
	#Hvis dette er en im alive-melding sett Is_alive
	#Hvis dette er en Cost-melding legg til i costlist