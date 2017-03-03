import Queue
from threading import Thread
from Lift_Control import receive_message, respond_to_message, do_work_based_on_button_press, broadcast_aliveness_and_check_aliveness_of_friends, driver, execute_order
from driver import lift_find_floor, listen_all_buttons
from Lift_struct import *
from Network import PORT

from Order_Module import print_orderlist

from File_Module import read_order_list_from_file

def set_ip_list(lift):

	MY_IP = get_my_ip()
	nr = 0

	if len(lift.ip_list) == 0:
		with lock:
			lift.ip_list = [MY_IP]
			lift.name = nr
	else:
		with lock:
			lift.ip_list = lift.ip_list + [MY_IP]
			nr = nr + 1
			lift.name = nr

	with lock:
		sorter(lift.ip_list)
		


def sorter(lst):
	new_list = []
	n = 0
	for index in range (len(lst)):
		for i in range (len(lst[index])):
			if lst[index][i] == '.':
				n += 1
				if n == 3:
					num = lst[index][i + 1] + lst[index][i + 2] 
					num = int(num)
					if len(lst[index]) == 15:
						num = lst[index][i + 1] + lst[index][i + 2] + lst[index][i + 3]
						num = int(num)
					new_list = new_list + [num]  

		n = 0

	for passesLeft in range(len(lst) - 1, 0, -1):
		for index in range(passesLeft):
			if new_list[index] > new_list[index + 1]:
				new_list[index], new_list[index + 1] = new_list[index + 1], new_list[index]
				lst[index], lst[index + 1] = lst[index + 1], lst[index]




def main():
	lift = Lift(0)
	driver.elev_init()
	lift.ip_list = ['129.241.187.38', '129.241.187.157', '129.241.187.145']
	lift.my_orders = read_order_list_from_file()
	internal_button_queue = Queue.Queue()
	external_button_queue = Queue.Queue()
	received_messages_queue = Queue.Queue()

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift, internal_button_queue, external_button_queue))
	thread_receive_message = Thread(target = receive_message, args = (lift, PORT,received_messages_queue))
	thread_respond_to_message = Thread(target = respond_to_message, args = (lift, received_messages_queue))
	thread_do_work_based_on_button_press = Thread(target = do_work_based_on_button_press, args = (lift,PORT, internal_button_queue, external_button_queue))
	thread_broadcast_aliveness_and_check_aliveness_of_friends = Thread(target = broadcast_aliveness_and_check_aliveness_of_friends, args = (lift,))
	
	thread_lift_find_floor.start()
	thread_listen_buttons.start() 
	thread_receive_message.start()
	thread_respond_to_message.start()
	thread_do_work_based_on_button_press.start()
	thread_broadcast_aliveness_and_check_aliveness_of_friends.start()

	while(1):
		execute_order(lift)



main()



#1. when an elevator dies, distribute orders between remaining elevators
#2. Find out why some messages are received twice
#3. Check whether lists are equal

