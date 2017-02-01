class Lift:
	def __init__(self, name):
		self.name = name
		self.is_alive = 1
		self.floor = 0
		self.direction = 0
		self.my_orders = []
		self.all_unexecuted_orders = []
		self.active_lifts = []
		self.ip_list = []

class Order:
	def __init__(self, floor, direction):
		self.floor = floor
		self.direction = direction



