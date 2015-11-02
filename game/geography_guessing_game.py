from __future__ import division
import random
import unittest
import sys
from gamestate import GameState, Mode

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
			and 'random' if you want a mix of both!")).lower()
		if user_input == "guess capital":
			return Mode.capital
		if user_input == "guess state":
			return Mode.state
		if user_input == "random":
			return Mode.random
		print "Learn to type, punk."

def ask_repeat_questions():
	while True:
		user_input = (raw_input("Type 'repeat' and enter if you want to see state/capital pairs more than once \
			and just enter if you do not want pairs to repeat.")).lower()
		if user_input == "repeat":
			return True
		if user_input == "":
			return False
		print "Invalid input, you bumble."

def ask_turns_goal():
	turns_goal = int(raw_input("How many rounds would you like to play? (We'll remind you when you're getting close!)")) 
	fancy_print("%d is a great number of rounds! Go you!" % turns_goal)
	return turns_goal

def asks_user_question(game): #could put asking and checking into same function
	(state, capital) = game.get_state_capital_pair()
	if game.mode == Mode.capital:  
		user_answer = raw_input("What is the capital of %s?" % state).lower()
		return user_answer, capital
	if game.mode == Mode.state:  
		user_answer = raw_input("What state has the capital %s?" % capital).lower() 
		return user_answer, state

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

def run():
	questions = state_capital_pairs()
	mode = ask_mode()
	repeat = ask_repeat_questions()
	turns_goal = ask_turns_goal()
	game = GameState(questions, mode, repeat, turns_goal)
	
	while True:
		game.update_mode()
		game.current_turn += 1
		turn_action = action_based_on_turns(game)
		if turn_action: #note: None evaluates to False
			fancy_print(turn_action)	
		fancy_print("This is turn number %d. Good luck!" % game.current_turn)
		
		user_answer, true_answer = asks_user_question(game)

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
		if user_answer == true_answer.lower():
			#repeat_questions = repeat_questions.remove(user_answer) #http://www.tutorialspoint.com/python/list_remove.htm
			game.right += 1
			fancy_print("Yay, you got points! Now at %d points with %d percent correct!" %(game.right, game.compute_percent()))
		else:
			game.wrong += 1
			fancy_print("Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(true_answer, game.right, game.compute_percent()))
		action_based_on_precent(game)
		
if __name__ == '__main__': # do all the stuff that should happen when this runs
	fancy_print("Welcome to Geography Guess-er-roo-y-time!")
	run()