from __future__ import division
import random
import unittest
import sys
from gamestate import Game, Mode

def fancy_print(string, i=1): 						
    # Prints out a string with i newlines after it
    print string
    print "\n"*i #use fancy_print instead of print

def question_to_answer_set():
	state_capital_pairs = Set()
	with open('state_capitals.txt', 'r').read().splitlines() as f:
		for line in f:
			state, capital = line.split(',')
			state_capital_pairs.add((state, capital)) #is a set
	return state_capital_pairs

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

def asks_user_question(game, key): #could put asking and checking into same function
	
	if game.get_mode() == Mode.capital:  
		user_answer = raw_input("What is the capital of %s?" % key).lower()
	if game.get_mode() == Mode.state:  
		user_answer = raw_input("What state has the capital %s?" % key).lower() 
	return user_answer

def action_based_on_turns(game): 
	if game.current_turn == game.turns_goal-3 and game.current_turn > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if game.current_turn == game.turn_goal+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if game.current_turn == 10 or game.current_turn == 20:
	  	return "You're doing a great job, keep going!"
	if game.current_turn == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you \
		really really want to learn these state capitals."

def action_based_on_precent(game):
	percent = game.get.percent()
	if percent <= 30:
		return "Keep trying! You'll get it!"
	if percent >= 60:
		return "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"

def run():
	questions = question_to_answer_set()
	mode = ask_mode()
	repeat = ask_repeat_questions()
	turns_goal = ask_turns_goal()
	game = Game(questions, mode, repeat, turns_goal)
	
	while True:
		turn_action = action_based_on_turns(game)
		if turn_action: #note: None evaluates to False
			fancy_print(turn_action)	
		fancy_print("This is turn number %d. Good luck!" % game.current_turn)
		
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