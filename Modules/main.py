from ctypes import *
from Lift_Control import *


def main():
	lift = Lift(2)
	driver.elev_init()
	lift.ip_list = ['129.241.187.145', '129.241.187.153', '129.241.187.151']
	lift.costlist = [-1, -1, -1]
	lift.active_lifts = [1, 1, 1]
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
