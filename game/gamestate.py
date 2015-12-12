from __future__ import division
import random
#from enum import Enum #but the docs say... https://docs.python.org/3/library/enum.html#enum.Enum


class GameState:
    def __init__(self, questions, mode, turns_goal):#removed repeat
        self.questions = questions
        self.mode = mode #guess state whole round, guess capital whole round, guess mix
        self.random = random
        #self.repeat = repeat #get same question more than once in game
        self.turns_goal = turns_goal
        self.current_turn = 0
        self.right = 0
        self.wrong = 0
        self.so_wrong_spell = 0
        self.little_wrong_spell = 0
        self.correct_spell = 0

    def update_mode(self):
        if self.random:
            self.mode = random.choice([Mode.state, Mode.capital])

    def get_state_capital_pair(self):
        index = random.randint(0,len(self.questions)-1)
        question = self.questions[index]
        #if not self.repeat: #T or F
        #    self.questions = self.questions[:index] + self.questions[index+1:]
        return question #can say get q, get answer because it knows what mode is (another option)

# use for testing
#   def print_2(self):
#       print 2

    def compute_percent_correct(self):
        if self.right + self.wrong == 0:
            return 0
        return (self.right/(self.right+self.wrong))*100

    def compute_percent_spelled_correct(self):
        return (self.correct_spell/(self.little_wrong_spell+self.so_wrong_spell+self.correct_spell))*100

    def compute_percent_spelled_almost_correct(self):
        return (self.little_wrong_spell/(self.little_wrong_spell+self.so_wrong_spell+self.correct_spell))*100

    def compute_percent_spelled_very_wrong(self):
        return (self.so_wrong_spell/(self.little_wrong_spell+self.so_wrong_spell+self.correct_spell))*100


class Mode(): #was Enum
    state = 0
    capital = 1
    random = 2
