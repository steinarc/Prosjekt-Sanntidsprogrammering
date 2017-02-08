from ctypes import *
from Lift_Control import *


def main():
	lift = Lift(1)
	driver.elev_init()
	lift.ip_list = ['10.22.69.248', '127.0.0.1', '127.0.0.1']

	#thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	#thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,))
	#thread_lift_find_floor.start()
	#thread_listen_buttons.start()
	#while(1):
	#	execute_order(lift)

	message = "1,Command,4 -1"
	message_type = classify_message(message)
	#print_order(order)
	#print message_type

	order = Order(3, -1)
	a = encode_command_message(lift, order)
	#print a
	heisnavn, order_received = decode_command_message(a)

	print_order(order_received)
	print(heisnavn)

	#send_and_spam_until_confirmation('10.22.69.248', 20018, b'Hei sveis')



main()