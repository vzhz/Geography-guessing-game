#note: requires 3.5 for duration of game in scoreboard

from __future__ import division
import random
import unittest
from difflib import SequenceMatcher
import sys
from gamestate import GameState, Mode
from game_helper_functions import *

def run():
    check_version()
    questions = state_capital_pairs()
    mode = ask_mode()
    #repeat = ask_repeat_questions()
    turns_goal = ask_turns_goal()
    game = GameState(questions, mode, turns_goal)#removed repeat

    time_start = time.time() #returns floating point number
    while True:
        game.update_mode()
        game.current_turn += 1
        make_scoreboard()
        turn_action = action_based_on_turns(game)
        if turn_action: #note: None evaluates to False
            fancy_print(turn_action)
        fancy_print("Turn number: %d. Good luck!" % game.current_turn)
        user_answer, true_answer = asks_user_question(game)
        check_if_want_quit_game()
        judge_spelling()

if __name__ == '__main__': # do all the stuff that should happen when this runs
    print(" ")
    fancy_print("Welcome to your customizable flashcards!")
    run()