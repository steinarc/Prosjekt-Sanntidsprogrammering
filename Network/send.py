from Network import *

#UDP_send('127.0.0.1', 20018, "Hei sveis")

order = Order(9,-1)
encoded = encode_order_message(order)
UDP_send_and_spam_until_confirmation('127.0.0.1', 20018, encoded, 10)


