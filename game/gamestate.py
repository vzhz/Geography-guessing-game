import random

class GameState:
    def __init__(self, questions, mode, turns_goal):
        self.QuestionFile = questionfile
        self.questions = questions
        self.mode = mode #guess state whole round, guess capital whole round, guess mix
        assert(mode in (Mode.first_half_pair, Mode.second_half_pair))
        self.random = random
        self.turns_goal = turns_goal
        self.current_turn = 0
        self.right = 0
        self.wrong = 0
        self.so_wrong_spell = 0
        self.little_wrong_spell = 0
        self.correct_spell = 0

    def update_mode(self):
        if self.random:
            self.mode = random.choice([Mode.first_half_pair, Mode.second_half_pair])

    def get_pair(self):
        index = random.randint(0,len(self.questions)-1)
        question = self.questions[index]
        #if not self.repeat: #T or F
        #    self.questions = self.questions[:index] + self.questions[index+1:]
        return question #can say get q, get answer because it knows what mode is (another option)

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
    first_half_pair = 0
    second_half_pair = 1
    random = 2

class QuestionFile():
    us_state_capital = 0
    french_food = 1
    metric = 2
    multiplication = 3
    user = 4