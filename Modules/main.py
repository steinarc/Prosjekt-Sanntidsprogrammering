import Queue
from threading import Thread
from Lift_Control import receive_message, respond_to_message, do_work_based_on_button_press, broadcast_aliveness_and_check_aliveness_of_friends, driver, execute_order
from driver import lift_find_floor, listen_all_buttons
from Lift_struct import *
from Network import PORT

from Order_Module import print_orderlist
from File_Module import read_order_list_from_file, write_time_to_file, read_time_from_file

import time
import os

LIFT_NUMBER = 0

#In main, process pairs are used so that if the program is terminated, the backup will continue
#This is done by writing and reading timestamps to a file called Time.txt

def backup():

	print("I am backup")
	time_now = 0
	time_prev = 1

	while time_now != time_prev:
		time_prev = read_time_from_file()
		time.sleep(2.1)
		time_now = read_time_from_file()
	
	primary()



def primary():
	global LIFT_NUMBER
	print("I am primary")
	os.system("gnome-terminal -x python main.py ")

	lift = Lift(LIFT_NUMBER)
	driver.elev_init()
	lift.ip_list = ['129.241.187.152', '129.241.187.144', '129.241.187.145']
	lift.my_orders = read_order_list_from_file()
	internal_button_queue = Queue.Queue()
	external_button_queue = Queue.Queue()
	received_messages_queue = Queue.Queue()

	thread_write_to_file = Thread(target = write_time_to_file)
	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift, internal_button_queue, external_button_queue))
	thread_receive_message = Thread(target = receive_message, args = (lift, PORT,received_messages_queue))
	thread_respond_to_message = Thread(target = respond_to_message, args = (lift, received_messages_queue))
	thread_do_work_based_on_button_press = Thread(target = do_work_based_on_button_press, args = (lift,PORT, internal_button_queue, external_button_queue))
	thread_broadcast_aliveness_and_check_aliveness_of_friends = Thread(target = broadcast_aliveness_and_check_aliveness_of_friends, args = (lift,))
	
	thread_write_to_file.start()
	thread_lift_find_floor.start()
	thread_listen_buttons.start() 
	thread_receive_message.start()
	thread_respond_to_message.start()
	thread_do_work_based_on_button_press.start()
	thread_broadcast_aliveness_and_check_aliveness_of_friends.start()

	while(1):
		execute_order(lift)



backup()



#1. when an elevator dies, distribute orders between remaining elevators
#2. Find out why some messages are received twice
#3. Check whether lists are equal

