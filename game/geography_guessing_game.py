import random
import unittest
import sys

def fancy_print(string, i=1): #does this automatically come after each string if //
							#you call it at the end?
    # Prints out a string with i newlines after it
    print string
    print "\n"*i #use fancy_print instead of print

def choose_order_in_case_of_placeholder():
	mode = random.choice([1, 2])
	return mode

def question_to_answer_dict(mode):
	state_capital = {}
	capital_state = {}
	f = open('state_capitals.txt', 'r').read().splitlines()
	for line in f:
		state, capital = line.split(',')
		state_capital[state] = capital
		capital_state[capital] = state

	if mode == 1:
		q_a_dict = state_capital #but this is an empty dict
	if mode == 2:
		q_a_dict = capital_state
	return q_a_dict

def compute_mode():
	#print sys.argv gives ['scrabble.py', '<whatever I typed after command in terminal>']
	mode_str = sys.argv[1].lower()
	while True:
		if mode_str == "guess capital" or mode_str == "capital":
			mode = 1
		elif mode_str == "guess state" or mode_str == "state":
			mode = 2
		elif mode_str == "mix it up!" or mode_str == "mix it up" or mode_str == "mix": 
			mode = choose_order_in_case_of_placeholder()
		#ask zulip folks if they know how to make !!! not matter, accept more variations
			#mode(state_capital, mode) #how to make random back and forth maybe start with random number and 
		#Should the game tell you "This is a state, give me the capital" in that case? Or should the player have to figure that out themself too?
		#figure out what should replace "state_capital" in line 19
		else:
			mode_str = raw_input("Please type or 'guess capital', 'guess state', or 'mix it up!' after name of program to start")
			continue
		break	
	return mode

def compute_repeat_questions():
	repeat_questions = sys.argv[2].lower()
	if repeat_questions == "repeat":
		repeat_questions = "repeat"
		#repeat_questions(, repeat_questions) #<--what there
	elif repeat_questions == "cover it all":
		repeat_questions = "cover it all"
		#repeat_questions(, repeat_questions) #<--what there
	else:
		print "Please type or 'repeat' or 'cover it all' after question type to start"
	return repeat_questions

def asks_user_question(mode, key):
	if mode == 1:  
		user_answer = raw_input("What is the capital of %s?" % key).lower()
	if mode == 2:  
		user_answer = raw_input("What state has the capital %s?" % key).lower() 
	return user_answer

def action_based_on_turns(turns, count): 
	if count == turns-3 and count > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if count == turns+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if count == 10 or count == 20:
	  	return "You're doing a great job, keep going!"
	if count == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you really really want to learn these state capitals."

def action_based_on_precent(percent):
	if percent <= 30:
		return "Keep trying! You'll get it!" #use return so you can run unit tests
	if percent >= 60:
		return "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"

def game(q_a_dict, mode, repeat_questions): 
	remaining_questions = list(range(1,51))
	points = 0
	count = 1.0 #float
	keys = q_a_dict.keys()
	turns = int(raw_input("How many rounds would you like to play? (We'll remind you when you're getting close!)")) 
	fancy_print("%d is a great number of rounds! Go you!" % turns)
	while True:
		if action_based_on_turns(turns, count): #note: None evaluates to False
			fancy_print(action_based_on_turns(turns, count))	
		fancy_print("This is turn number %d. Good luck!" % count)
		if repeat_questions == 'repeat':
			line_number = int(round(random.uniform(1,50))) #TODO len(question_to_answer_dict) not 50, check random
		if repeat_questions == 'cover it all':
			line_number = int(random.choice(remaining_questions)) 
		
		key = keys[line_number]
		value = q_a_dict[key]
		user_answer = asks_user_question(mode, key)

		if user_answer == "quit" or user_answer == "exit":
			user_wants_to_stay = raw_input("Are you sure you want to leave? (Y/N)")
			while True:	
				if user_wants_to_stay == "Y" or user_wants_to_stay == "y":
					fancy_print("Ok, hope to see you soon!")
					exit(0)
				if user_wants_to_stay == "N" or user_wants_to_stay == "n":
					fancy_print("Great! Let's do some more!")
					break
				else:
					user_wants_to_stay = raw_input("Please choose 'Y' to leave or 'N' to stay") 
			continue
		if user_answer == value.lower():
			#repeat_questions = repeat_questions.remove(user_answer) #http://www.tutorialspoint.com/python/list_remove.htm
			points += 1
			percent = (points/count)*100
			fancy_print("Yay, you got points! Now at %d points with %d percent correct!" %(points, percent))
		else:
			percent = (points/count)*100
			fancy_print("Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(value, points, percent))
		fancy_print(action_based_on_precent(percent))
		count += 1


if __name__ == '__main__': # do all the stuff that should happen when this runs
	fancy_print("Welcome to Geography Guess-er-roo-y-time!")
	mode = compute_mode()
	q_a_dict = question_to_answer_dict(mode)
	repeat_questions = compute_repeat_questions()
	game(q_a_dict, mode, repeat_questions) #global variables are sort of ok here, we suppose