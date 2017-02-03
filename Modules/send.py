from Network import *


lift = Lift(0)
order = Order(2,2)
encoded = encode_order_message(lift,order)
UDP_send_and_spam_until_confirmation('127.0.0.1', 20018, encoded)


