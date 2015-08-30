####
#tutorial instructions that jump-started this project: https://openhatch.org/wiki/Flash_card_challenge
####

import random
import unittest

state_capital = {}
capital_state = {}

f = open('state_capitals.txt', 'r').read().splitlines()

for line in f:
	pair = line.split(',')
	state_capital[pair[0]] = pair[1]
	capital_state[pair[1]] = pair[0]

print "Welcome to Geography Guess-er-roo-y-time!"

def action_based_on_turns(turns, count): 
	if count == turns-3 and count > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if count == turns+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if count == 10 or count == 20:
	  	return "You're doing a great job, keep going!"
	if count == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you really really want to learn these state capitals."

def asks_user_question(user_choice, key):
	if user_choice == 1:  
		user_answer = raw_input("What is the capital of %s?" % key).lower()
	else: 
		user_answer = raw_input("What state has the capital %s?" % key).lower()
	return user_answer

def action_based_on_precent(percent):
	if percent <= 30:
		return "Keep trying! You'll get it!" #use return so you can run unit tests
	if percent >= 60:
		return "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"

def state_or_capital_first(generic_dict, user_choice):
	points = 0
	count = 1.0 #float
	keys = generic_dict.keys()
	turns = int(raw_input("How many rounds would you like to play?")) 
	print "%d is a great number of rounds! Go you!" % turns
	while True:
		if action_based_on_turns(turns, count): #note: None evaluates to False
			print action_based_on_turns(turns, count)	
		print "This is turn number %d. Good luck!" % count
		line_number = int(round(random.uniform(1,50)))
		key = keys[line_number]
		value = generic_dict[key]
		user_answer = asks_user_question(user_choice, key)
		percent = (points/count)*100
		if user_answer == "quit" or user_answer == "exit":
			break #maybe break and ask them if they are sure
			dont_go = raw_input("Are you sure you want to leave? (Y/N)")
			if dont_go == "Y" or dont_go == "y":
				print "Ok, hope to see you soon!"
				exit(0)
			if dont_go == "N" or dont_go == "n":
				print "Great! Let's do some more!"
				continue
			else:
				print "Please choose 'Y' to leave or 'N' to stay" #test if this assigns y or n to dont_go
		if user_answer == value.lower():
			points += 1
			percent = (points/count)*100
			print "Yay, you got points! Now at %d points with %d percent correct!" %(points, percent)
		else:
			#print "user answer = %s" % user_answer
			#print "key.lower = %s" % key.lower()
			print "Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(value, points, percent)
		print action_based_on_precent(percent)
		count += 1
user_choice = raw_input("Would you like to be given a state and guess its capital or the other way around? If want to guess capitals, press 1. To guess states, press 2.")
if user_choice == "1" or user_choice == "2":
	pass
else: 
	user_choice = raw_input("Please (please please) type 1 for states->capitals or 2 for capitals->states. Jeezuuus, get it together.")
user_choice = int(user_choice)
if user_choice == 1:
	state_or_capital_first(state_capital, user_choice)
if user_choice == 2:
	state_or_capital_first(capital_state, user_choice)

####
#testing on other quiz files
#http://web.mit.edu/jesstess/www/IntermediatePythonWorkshop/metric.txt
#http://web.mit.edu/jesstess/www/IntermediatePythonWorkshop/french_food.txt
####