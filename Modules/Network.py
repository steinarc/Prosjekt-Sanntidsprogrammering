import socket
import select
import time
import Queue
from Lift_struct import *
from Queue_module import *
from threading import Thread

PORT = 20018

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
	sock_receive.close() #This is new, so remove hvis feil oppstaar
	return data

def send_and_spam_until_confirmation(remote_ip, port, data):

	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	confirmation = '0'

	return_queue = Queue.Queue() #Use queue to get the return value of the thread
	confirmation_thread = Thread(target = receive, args = (port + 1, 4, return_queue)) # 4 second timeout
	confirmation_thread.start()

	while(confirmation_thread.isAlive()): #While we wait for a confirmation send over and over again
		sock_send.sendto(data, (remote_ip, port))
		time.sleep(0.1)
	
	confirmation = return_queue.get()	
	print(confirmation)
	sock_send.close() #Fjern dette om feil plutselig oppstaar
	if (confirmation == '0'):
		print ("My friend has died")
	else:
		print("Message sent and my friend is still alive")

#Denne funksjonen ble laget fordi naar en heis mottar en melding vet vi
#ikke paa forhaand hvem som sendte den, det staar i selve meldinga
#tanken er at denne funksjonen skal kjoere i all evighet
#derfor puttes mottatt data inn i en koe, og ikke som returverdi
def receive_and_confirm(lift, port):

	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #!!!!!!!TEST!!!!!!!!!
	sock_receive.bind(('', port))	
	#sock_receive.setblocking(0)

	data = ''	
	data, addr = sock_receive.recvfrom(1024)
	

	if (len(data) > 0 and (data[0]).isdigit() == 1):
		remote_ip = lift.ip_list[int(data[0])]
		sock_send.sendto('1', (remote_ip, port + 1))
		sock_send.close()
		sock_receive.close()
		return (data)
	else:
		print("Received invalid message")
		return '0'
		















def get_my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])

def broadcast_my_IP(port):
#Steinars ip er 10.22.69.248
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
	
	while(True):
		s.sendto(MY_IP.encode(),('255.255.255.255',port))
		#print(MY_IP)
		time.sleep(1)
	s.close()