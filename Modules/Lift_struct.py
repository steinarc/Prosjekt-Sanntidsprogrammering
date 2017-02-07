class Lift:
	def __init__(self, name):
		self.name = name #corresponds to index in following lists
		self.is_alive = 1
		self.floor = 0
		self.direction = 0
		self.my_orders = []
		self.all_external_orders = []
		self.active_lifts = [] #[1 1 0]
		self.ip_list = [] #[123.289.477.387, 82.39.47.489, 78.42.03]
		self.costlist = []

class Order:
	def __init__(self, floor, direction):
		self.floor = floor
		self.direction = direction



