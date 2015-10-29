import random

class GameState:
	def __init__(self, mode, repeat):
		self.mode = mode
		self.repeat = repeat

	def get_mode(self):
		if self.mode == 2:
			return int((random.random)*2)
		return self.mode