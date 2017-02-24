import Queue
from threading import Thread
from Lift_Control import receive_message, respond_to_message, listen_external_buttons_and_send_order, broadcast_aliveness, driver, execute_order
from driver import lift_find_floor, listen_all_buttons
from Lift_struct import *
from Network import PORT

from Order_Module import print_orderlist

from File_Module import read_order_list_from_file


def main():
	lift = Lift(2)
	driver.elev_init()
	lift.ip_list = ['129.241.187.145', '129.241.187.153', '129.241.187.151']
	lift.my_orders = read_order_list_from_file()
	button_queue = Queue.Queue()
	received_messages_queue = Queue.Queue()

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,button_queue))
	thread_receive_message = Thread(target = receive_message, args = (lift, PORT,received_messages_queue))
	thread_respond_to_message = Thread(target = respond_to_message, args = (lift, received_messages_queue))
	thread_send_orders = Thread(target = listen_external_buttons_and_send_order, args = (lift,PORT, button_queue))
	thread_broadcast_aliveness = Thread(target = broadcast_aliveness, args = (lift,))
	
	thread_lift_find_floor.start()
	thread_listen_buttons.start() 
	thread_receive_message.start()
	thread_respond_to_message.start()
	thread_send_orders.start()
	thread_broadcast_aliveness.start()

	while(1):
		execute_order(lift)



main()


#1. Does the elevator reach where its supposed to go in time?
#2. Check whether lists are equal
#3. when an elevator dies, distribute orders between remaining elevators
#4. Find out why some messages are received twice