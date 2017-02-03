import socket
import sys
import time
import select
import Queue #funker ikke med python3 paa windows

def get_my_ip4_address():
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		print ('Socket created'.encode())
	except (socket.error, msg):
		print ('Failed to create socket. Error Code : '.encode() + str(msg[0]) + ' Message '.encode() + msg[1])
		sys.exit()

	s.connect(("gmail.com",80))
	return (s.getsockname()[0])
	
def get_my_ip():
	return socket.gethostbyname(socket.gethostname())
	
def UDP_create_socket():
	global s
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#print ('Socket created'.encode())
	except (socket.error, msg):
		print ('Failed to create socket. Error Code : '.encode() + str(msg[0]) + ' Message '.encode() + msg[1])
		sys.exit()

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	
	return s
	
def broadcast_my_IP(port):

	s = UDP_create_socket()
	
	MY_IP = get_my_ip()
	print(b'Broadcasting my ip address!')
	
	while(True):
		s.sendto(MY_IP.encode(),('255.255.255.255',port))
		#print(MY_IP)
		time.sleep(1)
	
	s.close()
	
def UDP_send(ip,port,msg):
	
	s = UDP_create_socket()
	s.sendto(msg, (ip, port))
	
	
def UDP_receive(port):

	s = UDP_create_socket()
		
	try :
		s.bind(('',port))
	except (socket.error, msg):
		print ('Failed to bind a socket. Error Code : '.encode() + str(msg[0]) + ' Message '.encode() + msg[1])
		sys.exit()
		
	m = s.recvfrom(1024)
	return (m[0])

def TCP_create_socket():
	global s
	
	try :
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#print ('Socket created'.encode())
	except (socket.error, msg):
		print ('Failed to create socket. Error Code : '.encode() + str(msg[0]) + ' Message '.encode() + msg[1])
		sys.exit()

	return s

def TCP_echo_server(port):
	s = TCP_create_socket()
	s.bind(('localhost',port)) 
	s.listen(1)
	conn, addr = s.accept()
	while 1:
		data = conn.recv(1024)
		if not data:
			break
		conn.sendall(data)
	conn.close()

	
def TCP_client(ip,port,msg):
	s = TCP_create_socket()
	s.connect(('localhost',port)) #finne ut om IP, min? din?
	s.sendall(msg) #msg.encode()
	data = s.recv(1024)
	s.close()
	return('Received'.encode(), repr(data))
	
def server(): #en non_blocking TCP server, koden tatt fra http://steelkiwi.com/blog/working-tcp-sockets/
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)
	server.bind(('localhost', 50000))
	server.listen(5)
	inputs = [server]
	outputs = []
	message_queues = {}

	while inputs:
		readable, writable, exceptional = select.select(inputs, outputs, inputs)
		for s in readable:
			if s is server:
				connection, client_address = s.accept()
				connection.setblocking(0)
				inputs.append(connection)
				message_queues[connection] = Queue.Queue()
			else:
				data = s.recv(1024)
				if data:
					message_queues[s].put(data)
					if s not in outputs:
						outputs.append(s)
				else:
					if s in outputs:
						outputs.remove(s)
				inputs.remove(s)
				s.close()
				del message_queues[s]

		for s in writable:
			try:
				next_msg = message_queues[s].get_nowait()
			except Queue.Empty:
				outputs.remove(s)
			else:
				s.send(next_msg)

		for s in exceptional:
			inputs.remove(s)
			if s in outputs:
				outputs.remove(s)
			s.close()
			del message_queues[s]
	
