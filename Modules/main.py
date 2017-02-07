from ctypes import *
from Lift_Control import *


def main():
	lift = Lift(0)
	driver.elev_init()

	thread_lift_find_floor = Thread(target = lift_find_floor, args = (lift,)) #maybe it is a shallow copy?? carefull!
	thread_listen_buttons = Thread(target = listen_all_buttons, args = (lift,))
	thread_lift_find_floor.start()
	thread_listen_buttons.start()

	while(1):
		execute_order(lift)



main()