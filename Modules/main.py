import Queue
from threading import Thread
from Lift_Control import receive_message, respond_to_message, do_work_based_on_button_press, broadcast_aliveness_and_check_aliveness_of_friends, driver, execute_order, init
from driver import lift_find_floor, listen_all_buttons
from Lift_struct import *
from Network import PORT, get_my_ip, broadcast_my_IP,receive

from Order_Module import print_orderlist

from File_Module import read_order_list_from_file

from Lock_Manager import *





def main():
	
	lift = init()

	#set_ip_list(lift)
	print(lift.ip_list)
	print(lift.name)


#	lift.ip_list = ['129.241.187.38', '129.241.187.157', '129.241.187.145']
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

