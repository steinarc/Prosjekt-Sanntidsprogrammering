from ctypes import *
from Lift_Control import *
from Message_Handling import *


def main():
	lift = Lift(0)
	driver.elev_init()
	lift.ip_list = ['129.241.187.151', '129.241.187.157', '129.241.187.148']
	lift.active_lifts = [1, 0, 0]
	button_queue = Queue.Queue()

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,button_queue))
	#thread_receive_message = Thread(target = receive_message_and_act, args = (lift, 20018))
	thread_send_orders = Thread(target = listen_external_buttons_and_send_order, args = (lift,20018, button_queue))
	
	thread_lift_find_floor.start()
	thread_listen_buttons.start() 
	#thread_receive_message.start()
	thread_send_orders.start()



	#send_and_spam_until_confirmation('10.22.69.248', 20018, b'Hei sveis')



main()