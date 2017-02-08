from ctypes import *
from Lift_Control import *


def main():
	lift = Lift(1)
	driver.elev_init()
	lift.ip_list = ['129.241.187.157', '129.241.187.151', '127.0.0.1']
	lift.active_lifts = [0, 0, 0]

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,))
	thread_receive_message = Thread(target = receive_message_and_act, args = (lift, 20018))
	thread_lift_find_floor.start()
	thread_listen_buttons.start()
	thread_receive_message.start()	

	while(1):
		print (lift.active_lifts)
		time.sleep(1)

	#send_and_spam_until_confirmation('10.22.69.248', 20018, b'Hei sveis')



main()