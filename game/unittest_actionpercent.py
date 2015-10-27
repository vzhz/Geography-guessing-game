import unittest

class Actiontest(unittest.TestCase):
	def test_action_blank_lines(self):
		blanklines = action_based_on_fancy_print() #how do I write a unit test for presence/absence of command
		self.assertEqual(blanklines, "\n"*i)
#def fancy_print(string, i=1): 						
#    # Prints out a string with i newlines after it
#    print string
#    print "\n"*i #use fancy_print instead of print

#def choose_order_in_case_of_placeholder():
#	mode = random.choice([1, 2])
#	return mode

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

# def compute_repeat_questions():
# 	repeat_questions = sys.argv[2].lower()
# 	if repeat_questions == "repeat":
# 		repeat_questions = "repeat"
# 		#repeat_questions(, repeat_questions) #<--what there
# 	elif repeat_questions == "cover it all":
# 		repeat_questions = "cover it all"
# 		#repeat_questions(, repeat_questions) #<--what there
# 	else:
# 		print "Please type or 'repeat' or 'cover it all' after question type to start"
# 	return repeat_questions

# def asks_user_question(mode, key):
# 	if mode == 1:  
# 		user_answer = raw_input("What is the capital of %s?" % key).lower()
# 	if mode == 2:  
# 		user_answer = raw_input("What state has the capital %s?" % key).lower() 
# 	return user_answer

class Actiontest(unittest.TestCase):
	def test_action_turns(self):
		keepgoing = action_based_on_current_turn(turns-3 and >1)
		self.assertEqual(keepgoing, "Almost to your rounds goal! Finallll pushhhh!")
		keepgoing = action_based_on_current_turn(turns+1)
		self.assertEqual(keepgoing, "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit.")
		keepgoing = action_based_on_current_turn(10 or 20)
		self.assertEqual(keepgoing, "You're doing a great job, keep going!")
		keepgoing = action_based_on_current_turn(60)
		self.assertEqual(keepgoing, "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you really really want to learn these state capitals.")

class Actiontest(unittest.TestCase):
	def test_action_percent(self):
		yousuck = action_based_on_percent(30)
		self.assertEqual(yousuck, "Keep trying! You'll get it!")
		yourock = action_based_on_percent(60)
		self.assertEqual(yousuck, "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?")




if __name__ == '__main__':
	unittest.main()