from gamestate import GameState
from game_helper_functions import *

def run():
    check_version()
    questions = state_capital_pairs() # make this variable so generic
    mode = ask_mode()
    turns_goal = ask_turns_goal()
    game = GameState(questions, mode, turns_goal) # removed repeat
    time_start = time.time() # returns floating point number

    while True:
        game.update_mode()
        game.current_turn += 1
        make_scoreboard()
        turn_action = action_based_on_turns(game)

        if turn_action: # None evaluates to False
            fancy_print(turn_action)

        fancy_print("Turn number: %d. Good luck!" % game.current_turn)

        user_answer, true_answer = asks_user_question(game)
        check_if_want_quit_game(user_answer, time_start, game)
        judge_spelling(true_answer, user_answer, game)

if __name__ == '__main__':
    print(" ")
    fancy_print("Welcome to your customizable flashcards!")
    run()