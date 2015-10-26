import random
import unittest
import sys

state_capital = {}
capital_state = {}

#print sys.argv gives ['scrabble.py', '<whatever I typed after command in terminal>']
mode = sys.argv[0].lower()
if mode == "guess capital" or mode == "capital":
	mode == 1
	mode(state_capital, mode)
if mode == "guess state" or mode == "state":
	mode == 2
 	mode(capital_state, mode)
if mode == "mix it up!" or mode == "mix it up" or mode == "mix": 
	mode == "placeholder"
#ask zulip folks if they know how to make !!! not matter, accept more variations
	mode(state_capital, mode) #how to make random back and forth maybe start with random number and 
#Should the game tell you "This is a state, give me the capital" in that case? Or should the player have to figure that out themself too?
#figure out what should replace "state_capital" in line 19
else:
	print "Please type or 'guess capital', 'guess state', or 'mix it up!' after name of program to start"

repeat_questions = sys.argv[1].lower()
if repeat_questions == "repeat":
	repeat_questions = "repeat"
	#repeat_questions(, repeat_questions) #<--what there
if repeat_questions == "cover it all":
	repeat_questions = "cover it all"
	#repeat_questions(, repeat_questions) #<--what there
else:
	print "Please type or 'repeat' or 'cover it all' after question type to start"

f = open('state_capitals.txt', 'r').read().splitlines()

def fancy_print(string, i=1): #does this automatically come after each string if //
							#you call it at the end?
    # Prints out a string with i newlines after it
    print string
    print "\n"*i #use fancy_print instead of print

for line in f:
	state, capital = line.split(',')

def action_based_on_turns(turns, count): 
	if count == turns-3 and count > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if count == turns+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if count == 10 or count == 20:
	  	return "You're doing a great job, keep going!"
	if count == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you really really want to learn these state capitals."

def asks_user_question(mode, key):
	if mode == 1:  
		user_answer = raw_input("What is the capital of %s?" % key).lower()
	if mode == 2:  
		user_answer = raw_input("What state has the capital %s?" % key).lower()
	if mode == "placeholder": #or random returns the equivelent of 1
		mode = random.choice([1, 2]) 
		if mode == 1:
			user_answer = raw_input("What is the capital of %s?" % key).lower()
		if mode == 2:
			user_answer = raw_input("What state has the capital %s?" % key).lower()
	return user_answer

def action_based_on_precent(percent):
	if percent <= 30:
		return "Keep trying! You'll get it!" #use return so you can run unit tests
	if percent >= 60:
		return "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"

def game(question_to_answer_dict, mode, repeat_questions): #question_to_answer_dict is first mentioned here
	remaining_questions = [range(1,51)]
	points = 0
	count = 1.0 #float
	keys = question_to_answer_dict.keys()
	print "\n"
	turns = int(raw_input("How many rounds would you like to play? (We'll remind you when you're getting close!)")) 
	print "%d is a great number of rounds! Go you!" % turns
	print "\n"
	while True:
		if action_based_on_turns(turns, count): #note: None evaluates to False
			print action_based_on_turns(turns, count)	
			print "\n"
		print "This is turn number %d. Good luck!" % count
		if repeat_questions == 'repeat':
			line_number = int(round(random.uniform(1,50))) #TODO len(question_to_answer_dict) not 50, check random
		if repeat_questions == 'cover it all':
			line_number = int(random.choice(remaining_questions)) 
		key = keys[line_number]
		value = question_to_answer_dict[key]
		user_answer = asks_user_question(state_or_capital_first, key) #investigate state_or_capt fi

		if user_answer == "quit" or user_answer == "exit":
			break
			user_wants_to_stay = raw_input("Are you sure you want to leave? (Y/N)")
			if user_wants_to_stay == "Y" or user_wants_to_stay == "y":
				print "Ok, hope to see you soon!"
				exit(0)
			if user_wants_to_stay == "N" or user_wants_to_stay == "n":
				print "Great! Let's do some more!"
				continue
			else:
				print "Please choose 'Y' to leave or 'N' to stay" #test if this assigns y or n to dont_go
		if user_answer == value.lower():
			repeat_questions = repeat_questions.remove(user_answer) #http://www.tutorialspoint.com/python/list_remove.htm
			points += 1
			percent = (points/count)*100
			print "Yay, you got points! Now at %d points with %d percent correct!" %(points, percent)
		else:
			print "Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(value, points, percent)
		print action_based_on_precent(percent)
		count += 1


if __name__ == '__main__':
	print "Welcome to Geography Guess-er-roo-y-time!"
	game(question_to_answer_dict, mode, repeat_questions)


    # do all the stuff that should happen when this runs

# done = False
# while not done:
# 	try:
# 		state_or_capital_first = int(raw_input("Would you like to be given a state and guess its capital or the other way around? If want to always guess capitals, press 1. To always guess states, press 2. To guess both, press 3."))
# 		if state_or_capital_first not in [1,2,3]:#in is for loop under hood
# 			print "Please (please please) type 1 for states->capitals, 2 for capitals->states, or 3 for both. Jeezuuus, get it together."
# 		else:
# 			done = True
# 			state_or_capital_first = int(state_or_capital_first)
# 			if state_or_capital_first == 1:
# 				state_or_capital_first(state_capital, state_or_capital_first)
# 			if state_or_capital_first == 2:
# 				state_or_capital_first(capital_state, state_or_capital_first)
# 			if state_or_capital_first == 3:
# 				state_or_capital_first(state_capital, state_or_capital_first)
# 				#Should the game tell you "This is a state, give me the capital" in that case? Or should the player have to figure that out themself too?
# 	except ValueError:
# 		print "1 and 2 are both numbers. I need a number.  Feed me numbers."

