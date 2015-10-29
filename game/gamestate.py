import random
from enum import Enum

class GameState:
	def __init__(self, mode, repeat):
		self.mode = mode
		self.repeat = repeat

	def get_mode(self):
		if self.mode == Mode.random:
			return (random.choice([Mode.state, Mode.capital])
		return self.mode

class Mode(Enum):
	state = 0
	capital = 1
	random = 2
