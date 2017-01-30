import socket

def my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])


#Declare the IP address that we will be trying to send our UDP messages to 
REMOTE_IP = my_ip() 
UDP_PORT = 6789
Message = "Hello, Server!"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(Message, (REMOTE_IP, UDP_PORT))
