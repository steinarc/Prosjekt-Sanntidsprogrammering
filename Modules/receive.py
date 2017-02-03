from Network import *

a = UDP_receive_and_confirm('127.0.0.1', 20018, 10)
classify_and_decode_message(a)


