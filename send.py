from Network import *
from Message_Handling import *


lift = Lift(0)
order = Order(2,-1)
lift.ip_list = ['127.0.0.1', '129.241.187.157', '129.241.187.148']

#send_command_message(lift, order, 1)
send_and_spam_until_confirmation('127.0.0.1', 20018, "encoded")


