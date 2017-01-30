import socket

def find_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])

def UDP_send(ip, port, data):
	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_send.sendto(Message, (REMOTE_IP, UDP_PORT))

def UDP_receive(ip, port):
	sock_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_receive.bind((MY_IP, UDP_PORT))

	while True:
		data, addr = serverSock.recvfrom(1024)
		print "Message: ", data
