from __future__ import division
import random
import unittest
from difflib import SequenceMatcher
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
