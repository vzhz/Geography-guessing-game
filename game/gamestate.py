from __future__ import division
import random
#from enum import Enum #but the docs say... https://docs.python.org/3/library/enum.html#enum.Enum


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
		if self.random:
			self.mode = random.choice([Mode.state, Mode.capital])

	def get_state_capital_pair(self):
		index = random.randint(0,len(self.questions)-1)
		question = self.questions[index]
		if not self.repeat: #T or F
			self.questions = self.questions[:index] + self.questions[index+1:]
		return question #can say get q, get answer because it knows what mode is (another option)

	def compute_percent(self):
		if self.right + self.wrong == 0:
			return 0
		return (self.right/(self.right+self.wrong))*100

class Mode(): #was Enum
	state = 0
	capital = 1
	random = 2
