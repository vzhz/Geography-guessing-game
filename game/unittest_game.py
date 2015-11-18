import unittest
import geography_guessing_game.py
import game_helper_functions.py

#logic, dependant on other parts of program

def fancy_print(string, i=1): 						
    # Prints out a string with i newlines after it
    print string
    print "\n"*i #use fancy_print instead of print

def state_capital_pairs():
	state_capital_pairs = []
	with open('state_capitals.txt', 'r') as f:
		splitlines = f.read().splitlines()
		for line in splitlines:
			state, capital = line.split(',')
			state_capital_pairs.append((state, capital))
	return state_capital_pairs
	# later, list comp

def ask_mode():
	while True:
		user_input = (raw_input("Type 'guess capital' if you want to guess capitals given states, \n \
			'guess state' if you want to guess states given capitals, \n \
			and 'random' if you want a mix of both! \n")).lower()
		if user_input == "guess capital":
			return Mode.capital
		if user_input == "guess state":
			return Mode.state
		if user_input == "random":
			return Mode.random
		print "Learn to type, punk. \n"

def ask_turns_goal():
	while True:
		turns_goal = int(raw_input("How many turns would you like to do today? \n")) 
		fancy_print("%d is a great number of rounds! Go you! \n" % turns_goal) 
		return turns_goal

def ask_repeat_questions():
	while True:
		repeat_questions = (raw_input("Type 'repeat' and enter if you want to see state/capital pairs more than \n \
			once, and enter if want to see state/capital pairs only once \n")) 
		return repeat_questions

def asks_user_question(game): #could put asking and checking into same function
	(state, capital) = game.get_state_capital_pair()
	if len(game.get_state_capital_pair()) > 0:
		if game.mode == Mode.capital:  
			user_answer = raw_input("What is the capital of %s? \n" % state) 
			return user_answer, capital
		if game.mode == Mode.state:  
			user_answer = raw_input("What state has the capital %s? \n" % capital)
			return user_answer, state
	else:
		pass

def action_based_on_turns(game): 
	if game.current_turn == game.turns_goal-3 and game.current_turn > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if game.current_turn == game.turns_goal+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if game.current_turn == 10 or game.current_turn == 20:
	  	return "You're doing a great job, keep going!"
	if game.current_turn == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you \
		really really want to learn these state capitals."

def action_based_on_precent(game):
	percent = game.compute_percent()
	if percent <= 30:
		fancy_print("Keep trying! You'll get it!")
	if percent >= 60:
		fancy_print("You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?")

#old after this
class Actiontest(unittest.TestCase):
	def test_action_blank_lines(self):
		blanklines = action_based_on_fancy_print() #how do I write a unit test for presence/absence of command
		self.assertEqual(blanklines, "\n"*blanklines) #maybe it doesn't need a test? how do you know?
#def fancy_print(string, i=1): 	#i is defined in the () for the first time	that makes sense!				
#    # Prints out a string with i newlines after it
#    print string
#    print "\n"*i #use fancy_print instead of print

	def test_action_random(self):
		random12 = random_action_1_2() #since it is just being called and not given an input is there anything to test?
		self.assertIn(random12, (1, 2))
#def choose_order_in_case_of_placeholder():
#	mode = random.choice([1, 2])
#	return mode

#assert functions are the tests
	def test_action_determine_dict(self):
		determinedict = action_based_on_mode(1)
		self.assertEqual(determinedict, state_capital) #does this have to be what is returned or what the returned thing equals?
		determinedict = action_based_on_mode(2)
		self.assertEqual(determinedict, capital_state)
# def question_to_answer_dict(mode):
# 	state_capital = {}
# 	capital_state = {}
# 	f = open('state_capitals.txt', 'r').read().splitlines()
# 	for line in f:
# 		state, capital = line.split(',')
# 		state_capital[state] = capital
# 		capital_state[capital] = state
#
#	 if mode == 1:
#	 	q_a_dict = state_capital #but this is an empty dict
#	 if mode == 2:
#	 	q_a_dict = capital_state
#	 return q_a_dict

	def test_action_determine_mode(self):
		determinemode = action_based_on_user_input("guess capital" or "capital")
		self.assertEqual(determinemode, 1)
		determinemode = action_based_on_user_input("guess state" or "state")
		self.assertEqual(determinemode, 2)
		determinemode = action_based_on_user_input("mix it up" or "mix")
		self.assertEqual(determinemode, 1 or 2)
# def compute_mode():
# 	#print sys.argv gives ['scrabble.py', '<whatever I typed after command in terminal>']
# 	mode_str = sys.argv[1].lower()
# 	while True:
# 		if mode_str == "guess capital" or mode_str == "capital":
# 			mode = 1
# 		elif mode_str == "guess state" or mode_str == "state":
# 			mode = 2
# 		elif mode_str == "mix it up!" or mode_str == "mix it up" or mode_str == "mix": 
# 			mode = choose_order_in_case_of_placeholder()
# 		#ask zulip folks if they know how to make !!! not matter, accept more variations
# 			#mode(state_capital, mode) #how to make random back and forth maybe start with random number and 
# 		#Should the game tell you "This is a state, give me the capital" in that case? Or should the player have to figure that out themself too?
# 		#figure out what should replace "state_capital" in line 19
# 		else:
# 			mode_str = raw_input("Please type or 'guess capital', 'guess state', or 'mix it up!' after name of program to start")
# 			continue
# 		break	
# 	return mode

	def test_action_repeat(self):
		determinerepeat = action_based_on_user_input("repeat") #does this need to be unique? (see last fcn)
		self.assertEqual(determinerepeat, "repeat")
		determinerepeat = action_based_on_user_input("cover it all")
		self.assertEqual(determinerepeat, "cover it all")
		determinerepeat = action_based_on_user_input() #how do I check "else" or do I just check the second time it runs when people type the right thing
		self.assertEqual(determinerepeat, "Please type or 'repeat' or 'cover it all' after question type to start")
# def compute_repeat_questions():
# 	repeat_questions = sys.argv[2].lower()
# 	if repeat_questions == "repeat":
# 		repeat_questions = "repeat"
# 		#repeat_questions(, repeat_questions) #<--what there
# 	elif repeat_questions == "cover it all":
# 		repeat_questions = "cover it all"
# 		#repeat_questions(, repeat_questions) #<--what there
# 	else:
# 		print "Please type or 'repeat' or 'cover it all' after question type to start" <--maybe return answer in fcn but actually print in game fcn
# 	return repeat_questions

# def asks_user_question(mode, key):
# 	if mode == 1:  
# 		user_answer = raw_input("What is the capital of %s?" % key).lower()
# 	if mode == 2:  
# 		user_answer = raw_input("What state has the capital %s?" % key).lower() 
# 	return user_answer


	def test_action_turns(self):
		keepgoing = action_based_on_current_turn(turns-3)
		self.assertEqual(keepgoing, "Almost to your rounds goal! Finallll pushhhh!")
		keepgoing = action_based_on_current_turn(turns+1)
		self.assertEqual(keepgoing, "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit.")
		keepgoing = action_based_on_current_turn(10 or 20)
		self.assertEqual(keepgoing, "You're doing a great job, keep going!")
		keepgoing = action_based_on_current_turn(60)
		self.assertEqual(keepgoing, "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you really really want to learn these state capitals.")

	def test_action_percent(self):
		yousuck = action_based_on_percent(30)
		self.assertEqual(yousuck, "Keep trying! You'll get it!")
		yourock = action_based_on_percent(60)
		self.assertEqual(yousuck, "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?")

if __name__ == '__main__':
	unittest.main()