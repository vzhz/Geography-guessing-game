from __future__ import division
import random
from enum import Enum


class GameState:
	def __init__(self, questions, mode, repeat, turns_goal):
		self.questions = questions
		self.mode = mode
		self.random = random
		self.repeat = repeat
		self.turns_goal = turns_goal
		self.current_turn = 0
		self.right = 0
		self.wrong = 0


	def update_mode(self):
		if self.random == Mode.random:
			self.mode = random.choice([Mode.state, Mode.capital]

	def get_state_capital_pair(self):
		question = self.questions.pop()
		if self.repeat: #T or F
			self.questions.add(question)
		return question #can say get q, get answer because it knows what mode is (another option)

	def compute_percent(self):
		if self.right + self.wrong == 0:
			return 0
		return (self.right//(self.right+self.wrong))*100




class Mode(Enum):
	state = 0
	capital = 1
	random = 2
