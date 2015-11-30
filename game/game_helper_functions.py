from __future__ import division
import random
import unittest
from difflib import SequenceMatcher
import sys
from gamestate import GameState, Mode
import sqlite3
import time #to tell how long playing
import datetime #date stamp

def fancy_print(string, i=1): 						
    # Prints out a string with i newlines after it
    print(string)
    print("\n"*i) #use fancy_print instead of print

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
		print("Learn to type, punk. \n")

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
	if game.current_turn == game.turns_goal-game.turns_goal/10 and game.current_turn > 1:
	  	return "Almost to your rounds goal! Finallll pushhhh!"
	if game.current_turn == game.turns_goal+1:
	  	return "Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit."
	if game.current_turn == game.turns_goal/10 or game.current_turn == game.turns_goal/5:
	  	return "You're doing a great job, keep going!"
	if game.current_turn == 60:
		return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you \
		really really want to learn these state capitals."

def action_based_on_percent(game):
	percent = game.compute_percent_correct()
	if percent <= 30:
		fancy_print("Keep trying! You'll get it!")
	if percent >= 60:
		fancy_print("You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?")

###end game
def make_scoreboard():
	if os.~/.geography_guessing_game.isfile('scores.db'):
		pass
	else:
		#create db file for scores
		conn = sqlite3.connect('scores.db')
		c = conn.cursor()
		c.execute("""CREATE TABLE scores 
					(name text, score integer, time unix, timer integer)""")
		return scores.db

def end_game():
	time_end = time.time() #end game timer
	pretty_time_of_game_play()
	update_scoreboard()
	game_summary()

def calculate_time_of_game_play():
	time_of_game_play = (time_end - time_start)
	return time_of_game_play #in seconds

def pretty_time_of_game_play(time_of_game_play):
	#time_of_game_play is in secs
	secs = int(time_of_game_play)
	if secs < 60:
		return '%d s'.format(secs)
	mins = secs / 60 
	secs -= mins * 60 #note: might get diff answer with modulo is using floats but this is an int, yay!
	if mins < 60:
		return '%d h %02d m'.format(mins, secs) #pads two digits with zero :00
	hours = mins / 60
	mins -= hours * 60
	if hours < 24:
		return '%d h %02d m %02d'.format(hours, mins, secs)
	days = hours / 24
	hours -= days * 24
	return '%d d %02d h %02d m %02d'.format(days, hours, mins, secs)


def update_scoreboard(scores.db):
	#ask for users name
	name = raw_input("What be your flashcard-masterin' name, you little badass?")
	#insert row of data (once per game, at end)
	c.execute("INSERT INTO scores VALUES (name, game.right, datetime.datetime.now(datetime.timezone.utc), pretty_time_of_game_play")
	#save row just added
	conn.commit()
	#return scoreboard
	return scores.db
	#close connection
	conn.close()

def game_summary(scores.db):
	threshold_need_to_memorize = 60 #should I ask user how mean we should be re: spelling before we decide they weren't spelling the right word at all? maybe we should have difficulty levels
	update_scoreboard() 
	print("Total points: %d" %(game.right))
	print("Percent correct: %d" %(game.compute_percent()))
	print("Percent spelled correct: %d" %(game.compute_percent_spelled_correct()))
	print("Percent spelled almost correct: %d" %(compute_percent_spelled_almost_correct()))
	if (game.compute_percent_spelled_correct() + compute_percent_spelled_almost_correct()) < threshold_percent_need_to_memorize:
		print("You spelled %d very wrong, so I expect you were typing entirely wrong answers. Better hit the flashcards again!" %(compute_percent_spelled_very_wrong))
