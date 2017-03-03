import time
import Queue
from ctypes import *
from threading import Thread
from Lift_struct import *
from Order_Module import add_order_to_all_external_orders, add_order_to_my_orders, order_index_in_list, print_orderlist
from driver import lift_move_direction, set_external_lamp, set_internal_lamp, lift_stop
from Message_Handling import *
from Network import receive_and_confirm, set_ip_list, broadcast_my_IP, receive, get_my_ip, PORT, receive_IP
from Lock_Manager import lock
from Cost import calculate_cost, costlist_is_full, find_lift_with_minimal_cost
from File_Module import delete_order_from_file

driver = CDLL("./../driver/libdriver.so")

#Interface functions

def init():
	
	lift = Lift(0)
	MY_IP = get_my_ip()
	lift.ip_list = ['129.241.187.156', '129.241.187.160']

	queue = Queue.Queue()
	driver.elev_init()

	thread_broadcast = Thread(target = broadcast_my_IP, args = (lift, PORT))
	thread_receive = Thread(target = receive_IP, args = (lift, PORT, queue))
	#thread_list = Thread(target = set_ip_list, args = (lift, queue))

	thread_receive.start()
	thread_broadcast.start()
	#thread_list.start()

	while (len(lift.ip_list) != 3):
		set_ip_list(lift, queue)

	thread_receive.join()
	thread_broadcast.join()

	for n in range (len(lift.ip_list)):
		if (lift.ip_list[n] == MY_IP):
			with lock:
				lift.name = n

	return lift


def execute_order(lift):
	if (len(lift.my_orders) > 0):
		lift_go_to_floor(lift, lift.my_orders[0].floor, 0)
		if (lift.floor == lift.my_orders[0].floor):
			send_executed_message(lift,lift.my_orders[0])
			set_external_lamp(lift.my_orders[0],0)
			set_internal_lamp(lift.my_orders[0],0)
			delete_order_from_file(Order(lift.my_orders[0].floor, 0))
			index = order_index_in_list(lift.my_orders[0], lift.all_external_orders)
			if (index != -1):
				with lock:
					lift.all_external_orders.pop(index)
			with lock:
				lift.my_orders.pop(0)


def do_work_based_on_button_press(lift,port,internal_button_queue, external_button_queue):
	while(1):
		order_sent_successfully = False
		if (lift.stopped == 1):
			break
		if (external_button_queue.empty() == 0):
			order = external_button_queue.get()
			add_order_to_all_external_orders(lift, order)
			with lock:
				lift.costlist[lift.name] = calculate_cost(lift,order)
			order_sent_sucessfully = send_order_message(lift,order)
			if (order_sent_sucessfully == False):
				print("List of orders:")
				print_orderlist(lift.all_external_orders)
				add_order_to_my_orders(lift,order)
				set_external_lamp(order,1)
		if (internal_button_queue.empty() == 0):
			order = internal_button_queue.get()
			add_order_to_my_orders(lift, order)



def broadcast_aliveness_and_check_aliveness_of_friends(lift):
	prev_active_lifts = [1, 1, 1]	
	while(1):
		send_Im_alive_message(lift)
		if (prev_active_lifts != lift.active_lifts): #If a lift has died or resurrected
			for i in range (0, 3):
				if (i != lift.name):
					if (prev_active_lifts[i] == 1 and lift.active_lifts[i] == 0):
						if ((i + 1) % 3 == lift.name or lift.active_lifts[(i+1) % 3] == 0): #2 is backup for 1, 1 is backup for 0 and 0 for 2
							for x in range (0, len(lift.all_external_orders)):
								add_order_to_my_orders(lift, lift.all_external_orders[x])

		for  i in range(0, 3):
			prev_active_lifts[i] = lift.active_lifts[i]

		time.sleep(1)


		

def receive_message(lift, port, received_messages_queue): #will always be run as a thread ALWAYS!
	while(1):
		message = receive_and_confirm(lift, port) # The function will wait here until something is received
		with lock:
			received_messages_queue.put(message)



def respond_to_message(lift,received_messages_queue):
	while(1):
		if (received_messages_queue.empty() == 0):

			message = received_messages_queue.get()
			print(message)
			message_type = classify_message(message)

			if (message_type == 'Order'):
				print("Order message received")
				sending_lift, order = decode_order_message(message)
				add_order_to_all_external_orders(lift, order)
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
				with lock:
					lift.costlist[lift_name] = cost
				if (costlist_is_full(lift)):
					lift_with_minimal_cost_name = find_lift_with_minimal_cost(lift)
					if (lift_with_minimal_cost_name == lift.name):
						with lock:
							add_order_to_my_orders(lift, order)
					else:
						send_command_message(lift, order, lift_with_minimal_cost_name)
					set_external_lamp(order, 1)
					with lock:	
						lift.costlist = [-1, -1, -1]

			elif(message_type == 'Command'):
				print("Command message received")
				lift_name, order = decode_command_message(message)
				set_external_lamp(order, 1)
				with lock:
					add_order_to_my_orders(lift, order)

			elif(message_type == 'Executed'):
				print("Executed message received")
				lift_name, order = decode_executed_message(message)
				set_external_lamp(order, 0)
				index = order_index_in_list(order, lift.all_external_orders)
				if (index != -1):
					with lock:
						lift.all_external_orders.pop(index)
					print("Order successfully removed")


#Additional functions

def lift_go_to_floor(lift, floor, timeout):
	prev_floor = -1
	motor_is_set = 0
	declared_dead = 0
	starttime = time.time()
	while(1):
		if (lift.stopped == 1):
			lift_stop(lift)
			break
		else:
			if (lift.floor == floor and driver.elev_get_floor_sensor_signal() == floor ):
				lift_stop(lift)
				driver.elev_set_door_open_lamp(1)
				time.sleep(2)
				driver.elev_set_door_open_lamp(0)
				lift.is_alive = 1
				break
			if (lift.floor < floor and (motor_is_set == 0)):
				lift_move_direction(lift, 1)
				motor_is_set = 1
				starttime = time.time()
			elif (lift.floor > floor and motor_is_set == 0):
				lift_move_direction(lift, -1)
				motor_is_set = 1
				starttime = time.time()
			if (time.time() - starttime > 10 and declared_dead == 0):
				print("I am dead")
				lift.is_alive = 0
				declared_dead = 1

			prev_floor = lift.floor