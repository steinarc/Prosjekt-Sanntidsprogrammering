from Network import *

lift = Lift(1)
order = Order(2,-1)
lift.ip_list = ['127.0.0.1', '127.0.0.1', '129.241.187.148']


#a = receive_and_confirm('127.0.0.1', 20018)
#a = receive_and_confirm(lift, 20018)
#print(a)
#classify_and_decode_message(a)

#print(find_ip())


a = receive_and_confirm(lift, 20018)
print(a)