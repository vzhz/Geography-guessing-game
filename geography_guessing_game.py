import random
import unittest

state_capital = {}
capital_state = {}

f = open('state_capitals.txt', 'r').read().splitlines()

for line in f:
	pair = line.split(',')
	state_capital[pair[0]] = pair[1]
	capital_state[pair[1]] = pair[0]

print "\n"
print "Welcome to Geography Guess-er-roo-y-time!"
print "\n"

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
	print "\n"
	turns = int(raw_input("How many rounds would you like to play?")) 
	print "%d is a great number of rounds! Go you!" % turns
	print "\n"
	while True:
		if action_based_on_turns(turns, count): #note: None evaluates to False
			print action_based_on_turns(turns, count)	
			print "\n"
		print "This is turn number %d. Good luck!" % count
		line_number = int(round(random.uniform(1,50))) #len(generic_dict) not 50, check random
		key = keys[line_number]
		value = generic_dict[key]
		user_answer = asks_user_question(user_choice, key)
		percent = (points/count)*100
		if user_answer == "quit" or user_answer == "exit":
			break
			dont_go = raw_input("Are you sure you want to leave? (Y/N)")
			print "\n"
			if dont_go == "Y" or dont_go == "y":
				print "Ok, hope to see you soon!"
				print "\n"
				exit(0)
			if dont_go == "N" or dont_go == "n":
				print "Great! Let's do some more!"
				print "\n"
				continue
			else:
				print "Please choose 'Y' to leave or 'N' to stay" #test if this assigns y or n to dont_go
				print "\n"
		if user_answer == value.lower():
			points += 1
			percent = (points/count)*100
			print "Yay, you got points! Now at %d points with %d percent correct!" %(points, percent)
			print "\n"
		else:
			print "Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(value, points, percent)
			print "\n"
		print action_based_on_precent(percent)
		print "\n"
		count += 1
done = False
while not done:
	try:
		user_choice = int(raw_input("Would you like to be given a state and guess its capital or the other way around? If want to guess capitals, press 1. To guess states, press 2."))
		if user_choice not in [1,2]:#in is for loop under hood
			print "Please (please please) type 1 for states->capitals or 2 for capitals->states. Jeezuuus, get it together."
			print "\n"
		else:
			done = True
			user_choice = int(user_choice)
			if user_choice == 1:
				state_or_capital_first(state_capital, user_choice)
			if user_choice == 2:
				state_or_capital_first(capital_state, user_choice)
	except ValueError:
		print "1 and 2 are both numbers. I need a number.  Feed me numbers."

