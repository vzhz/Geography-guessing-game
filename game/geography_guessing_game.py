from __future__ import division
import random
import unittest
from difflib import SequenceMatcher
import sys
from gamestate import GameState, Mode
from game_helper_functions import *
import pickle 

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
					game_summary()
					exit(0)
				if user_wants_to_stay == "N" or user_wants_to_stay == "n":
					fancy_print("Great! Let's do some more!")
					break
				else:
					user_wants_to_stay = raw_input("Please choose 'Y' to leave or 'N' to stay") 
			continue
		#maybe test user answer fcn
		#if user_answer == true_answer.lower():
		min_spelling_ratio = 0.75 #later allow user to pass it in, so they can decide how correct counts
		#maybe I should have difficulty levels that have defaults of harder min_spelling_ratios, etc. and user choses their level
		how_correct_spell = SequenceMatcher(None, true_answer.lower(), user_answer.lower())
		spelling_ratio = how_correct_spell.ratio()
		if spelling_ratio >= min_spelling_ratio:
			#repeat_questions = repeat_questions.remove(user_answer) #http://www.tutorialspoint.com/python/list_remove.htm
			game.right += 1
			if spelling_ratio == 1:
				game.correct_spell += 1
			else:
				game.little_wrong_spell += 1
				print ("Your spelling is so close! We'll call it good!")
			fancy_print("Yay, you got points! Now at %d points with %d percent correct!" %(game.right, game.compute_percent_correct()))
		else:
			game.wrong += 1
			game.so_wrong_spell += 1
			fancy_print("Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(true_answer, game.right, game.compute_percent_correct()))
		action_based_on_precent(game)

		
		
if __name__ == '__main__': # do all the stuff that should happen when this runs
	print " "
	fancy_print("Welcome to Geography Guessing Game!")
	run()