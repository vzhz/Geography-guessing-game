from gamestate import GameState
from game_helper_functions import *

def run():
    check_version()
    file_choice = choose_flashcard_file()
    create_pairs_table()
    name = ask_user_name()
    message_ask_for_second_half_pair, message_ask_for_first_half_pair, pairs_list = read_flashcards_set(file_choice, name)
    mode = ask_mode()
    turns_goal = ask_turns_goal()
    game = GameState(pairs_list, name, mode, turns_goal)
    time_start = time.time() # returns floating point number

    while True:
        game.current_turn += 1
        make_scoreboard()
        turn_action = action_based_on_turns(game)

        if turn_action: # None evaluates to False
            fancy_print(turn_action)

        fancy_print("Turn number: %d. Good luck!" % game.current_turn)

        user_answer, true_answer = asks_user_question(game, message_ask_for_second_half_pair, message_ask_for_first_half_pair)
        check_if_want_quit_game(user_answer, time_start, game)
        evaluate_user_answer_spelling(true_answer, user_answer, game)

if __name__ == '__main__':
    print(" ")
    fancy_print("Welcome to your customizable flashcards!")
    run()