from ctypes import *
from Lift_Control import *
from Message_Handling import *


def main():
	lift = Lift(0)
	driver.elev_init()
	lift.ip_list = ['129.241.187.157', '129.241.187.145', '129.241.187.151']
	lift.costlist = [-1, -1, -1]
	lift.active_lifts = [1, 1, 1]
	button_queue = Queue.Queue()
	received_messages_queue = Queue.Queue()

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,button_queue))
	thread_receive_message = Thread(target = receive_message, args = (lift, 20018,received_messages_queue))
	thread_respond_to_message = Thread(target = respond_to_message, args = (lift, received_messages_queue))
	thread_send_orders = Thread(target = listen_external_buttons_and_send_order, args = (lift,20018, button_queue))
	
	thread_lift_find_floor.start()
	thread_listen_buttons.start() 
	thread_receive_message.start()
	thread_respond_to_message.start()
	thread_send_orders.start()

	while(1):
		execute_order(lift)



main()