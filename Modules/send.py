from Network import *
from Message_Handling import *


lift = Lift(0)
order = Order(2,-1)
encoded = encode_executed_message(lift,order)
send_and_spam_until_confirmation('127.0.0.1', 20018, encoded)


