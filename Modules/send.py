from Network import *


lift = Lift(0)
order = Order(2,-1)
encoded = encode_order_message(lift,order)
UDP_send_and_spam_until_confirmation('129.241.187.153', 20018, encoded)


