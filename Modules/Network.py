import socket
import select
import time
import Queue
from Lift_struct import *
from threading import Thread
from Lock_Manager import lock

PORT = 20298

#Interface functions

def send_and_spam_until_confirmation(lift, other_lift, port, data):

	remote_ip = lift.ip_list[other_lift]
	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	success = False
	confirmation = '0'

	return_queue = Queue.Queue() #Use queue to get the return value of the thread
	confirmation_thread = Thread(target = receive, args = (port + 1, 4, return_queue)) # 4 second timeout
	confirmation_thread.start()

	while(confirmation_thread.isAlive()): #While we wait for a confirmation send over and over again
		sock_send.sendto(data, (remote_ip, port))
		time.sleep(0.1)
	
	confirmation = return_queue.get()	
	sock_send.close() #Fjern dette om feil plutselig oppstaar
	if(confirmation == remote_ip):
		print("Message sent and " + str(other_lift) + " is still alive")
		success = True
	else:
		print ("My friend " + str(other_lift) + " is a deadlift")
		with lock:
			lift.active_lifts[other_lift] = 0
		success = False
	return success

#Denne funksjonen ble laget fordi naar en heis mottar en melding vet vi
#ikke paa forhaand hvem som sendte den, det staar i selve meldinga
#tanken er at denne funksjonen skal kjoere i all evighet
#derfor puttes mottatt data inn i en koe, og ikke som returverdi
def receive_and_confirm(lift, port):

	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Testing binding from multiple places
	sock_receive.bind(('', port))	
	#sock_receive.setblocking(0)

	data = ''	
	data, addr = sock_receive.recvfrom(1024)

	if (len(data) > 0 and (data[0]).isdigit() == 1):
		remote_ip = lift.ip_list[int(data[0])]
		sock_send.sendto(lift.ip_list[lift.name], (remote_ip, port + 1))
		sock_send.close()
		sock_receive.close()
		return (data)
	else:
		print("Received invalid message")
		return '0'
		

def receive(port, timeout, return_queue):
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
	sock_receive.bind(('', port)) #maa bruke egen IP her
	#sock_receive.setblocking(0)	#Kanskje vi ikke trenger denne for timeout likevel
	data = '0'


	ready = select.select([sock_receive], [], [], timeout)
	if (ready[0]):
		data, addr = sock_receive.recvfrom(1024)
	if(data == '0'):
		print("Nothing was received")	

	return_queue.put(data)
	sock_receive.close()
	return data

def receive_IP(lift, port, return_queue):
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
	sock_receive.bind(('', port)) #maa bruke egen IP her


	while len(lift.ip_list) != 3:
		data, addr = sock_receive.recvfrom(1024)
		return_queue.put(data)


	sock_receive.close()
	return data		

def set_ip_list(lift, ip_queue):

	ip = ip_queue.get()
	if len(lift.ip_list) == 0:
		with lock:
			lift.ip_list = [ip]

	else:

		is_in_list = False
		for i in range (len(lift.ip_list)):
			if lift.ip_list[i] == ip:
				is_in_list = True

		if is_in_list == False:
			with lock:
				lift.ip_list = lift.ip_list + [ip]


	with lock:
		sorter(lift.ip_list)
		


#Additional functions

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

def get_my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])

def broadcast_my_IP(lift, port):
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#print ('Socket created'.encode())
	except (socket.error, msg):
		print ('Failed to create socket. Error Code : '.encode() + str(msg[0]) + ' Message '.encode() + msg[1])
		sys.exit()

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	MY_IP = get_my_ip()
	print(b'Broadcasting my ip address!')
	

	while len(lift.ip_list) != 3 :
		s.sendto(MY_IP.encode(),('255.255.255.255',port))
		#time.sleep(3)
		#break

	print('Broadcasting done!')
	s.close()