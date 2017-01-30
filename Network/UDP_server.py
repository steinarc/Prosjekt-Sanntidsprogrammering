import socket

def my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	return (s.getsockname()[0])


#Listening on our defined IP address 
MY_IP = my_ip()
UDP_PORT = 6789


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((MY_IP, UDP_PORT))

while True:
	data, addr = serverSock.recvfrom(1024)
	print "Message: ", data
