"""Core functionality for flashcard game."""

# python std library
import datetime
from difflib import SequenceMatcher
import os
import random
import sqlite3
import sys
import time

# libraries
from curtsies.fmtfuncs import red, bold, blue

# my code
from gamestate import Mode



def check_version():
    """Tests if Python version is >= 3.5.x and print user instructions if it is not."""

    message = (
        "Hey asshole, did you even read the README? You're using the wrong Python "
        "version and are going to be very sad when I don't save your score."
    )
    prompt = "Would you like to leave and restart after opening with the correct version [y,n]?:"

    if sys.version_info[0] < 3 or (sys.version_info[0] == 3 and sys.version_info[1] < 5):
        print(red(message))
        if input(prompt).lower() in ["y", "yes"]:
            print(bold("Remember to type 'python3'"))
            exit()


def fancy_print(string, i=1):
    """Adds i extra lines after printed message."""

    print(string + "\n" * i)


def choose_flashcard_file():
    """Reads flashcard text file and assigns the pairs to list"""

    user_file_name = input(
        "\nWhat flashcards would you like to practice today?"
        "\n"
        "\n  1: If you want to learn US state capitals."
        "\n  2: If you want to learn a few words in French."
        "\n  3: If you want to learn metric/SI conversions."
        "\n  4: If you want to learn a few multiplication tables."
        "\n  5: If want to load your own file."
        "\n"
        "\nType your choice [1,2,3,4,5]: "
        )

    if user_file_name == "1":
        file_choice = "us_state_capitals.txt"
    elif user_file_name == "2":
        file_choice = "frenchfood_englishfood.txt"
    elif user_file_name == "3":
        file_choice = "metric.txt"
    elif user_file_name == "4":
        file_choice = "multiplication.txt"
    elif user_file_name == "5":
        print(
            "\n"
            "\nI see you want to add a new file. First, you need to decide the questions you will "
            "be asked."
            "\n"
            "\nLet's make sure you understand the style and formatting of the questions."
            "\nYou'll get to write a few lines of your own code!"
            "\n"
            "\nWe'll ask quiz you by giving you one 'side' of your flashcard and you tell us the "
            "other 'side'."
            "\n"
            "\nFor example, for pairs formatted <state, capital>, we might ask:"
            "\n  What is the capital of Nebraska? [In code: 'What is the capital of %s? ']"
            "\n  or"
            "\n  What state has the capital Lincoln? [In code: 'What state has the capital %s? ']"
            "\n     Don't worry about the %s! It's just you telling the question you love it!"
            "\n"
            "\n"
            "\nIn the file (starting on first line):"
            "\n"
            "\n  Question asking for second half of pair"
            "\n  Question asking for first half of pair"
            "\n  First half of pair, Second half of Pair"
            "\n  First half of pair, Second half of Pair"
            "\n  First half of pair, Second half of Pair"
            "\n  ..."
            "\n"
            "\nFile naming:"
            "\n  name.txt"
            "\n"
            "\nSave file to the same folder as the game."
            "\n"
            )
        file_choice = input("What is the name (including extention) of your file?")
    else:
        print("Learn to type, punk. Choose [1,2,3,4,5]\n")
        file_choice = choose_flashcard_file()
    return file_choice

        # pause for the user to finish writing their thing and then have them confirmed that they are happy and have their thing written and saved


def create_pairs_table():
    if not os.path.isfile('pairs.db'): # technically, shouldn't hardcode db filename, use variable
        conn = sqlite3.connect('pairs.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE pairs
                    (name text, pair text, right integer, wrong integer, ratio blob)""")
        conn.commit()
        conn.close()
        # needs logic to give more or less
        # seperate pair into first and second half of pair


def ask_user_name():
    name = input("What be your flashcard-masterin' name, you little badass?")
    return name


def read_flashcards_set(user_file, name):
    pairs_list = []
    with open(user_file, 'r') as f:
        message_ask_for_second_half_pair = f.readline()
        message_ask_for_first_half_pair = f.readline()
        for line in f.read().splitlines():
            pairs_list.append(line.split(','))
            conn = sqlite3.connect('pairs.db')
            c = conn.cursor()
#            line_insert = ("INSERT INTO pairs VALUES (\"%s\", \"%s\", "%d", "%d", "%d")"
#                           %(name, pair, <counter for this pair.right>, <counter for this pair.wrong>, <output of ratio calc>))
#            c.execute(line_insert)
            conn.commit()
            conn.close()
    return message_ask_for_second_half_pair, message_ask_for_first_half_pair, pairs_list

def ask_mode():
    """Asks user if s/he would like to respond with the first or second element of the pair
       when given the other."""

    while True:
        user_input = input(
            "\nWould you like to guess capitals given states or vice versa?"
            "\n"
            "\n  1: If you want to guess capitals given states."
            "\n  2: If you want to guess states given capitals."
            "\n  3: If you want a mix of both!"
            "\n"
            "\nType your choice [1,2,3]: "
        ).lower()

        if user_input == "1":
            return Mode.second_half_pair
        if user_input == "2":
            return Mode.first_half_pair
        if user_input == "3":
            return Mode.random

        print("Learn to type, punk.\n")


def ask_turns_goal():
    """Asks user how many turns they plan to do."""

    turns_goal = int(input("How many turns would you like to do today? \n"))
    return turns_goal


def asks_user_question(game, message_ask_for_second_half_pair,  message_ask_for_first_half_pair):
    """Gives user one side of the pair and asks them to type other side of the pair."""

    first_half_pair, second_half_pair = game.get_pair()

    if game.mode == Mode.random:
        mode = random.choice([Mode.first_half_pair, Mode.second_half_pair])
    else:
        mode = game.mode

    if mode == Mode.second_half_pair:
        user_answer = input(message_ask_for_second_half_pair % first_half_pair)
        return user_answer, second_half_pair
    elif mode == Mode.first_half_pair:
        user_answer = input(message_ask_for_first_half_pair % second_half_pair)
        return user_answer, first_half_pair


def action_based_on_turns(game):
    """Prints message to user based on number of turns the user has completed."""

    def handle_near_to_goal():
        if game.current_turn == game.turns_goal - game.turns_goal / 10 and game.current_turn > 1:
            print(blue("Almost to your rounds goal! Finallll pushhhh!"))

    def handle_after_goal():
        if game.current_turn == game.turns_goal + 1:
            print("Would you like to continue? Practice makes perfect! Type 'quit' to exit.")

    def handle_encourage_to_goal():
        if game.current_turn == game.turns_goal / 10 or game.current_turn == game.turns_goal / 5:
            print(blue("You're doing a great job, keep going!"))

    def handle_too_many_turns():
        if game.current_turn == 100:
            print("Really, you should stop.  It's bedtime. Type 'quit' anytime to exit."
                  "Or continue, because you reeeally want to learn the things (you're awesome!).")

    handle_near_to_goal()
    handle_after_goal()
    handle_encourage_to_goal()
    handle_too_many_turns()


def action_based_on_percent(game):
    """Prints feedback for user based on performance (percent correct)."""

    you_suck_message = [
        "Keep trying! You'll get it!",
        "Come on, human.",
        "Try harder?"
        ]
    you_rock_message = [
        "WAY TO GO!",
        "You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?",
        "WELL DONE!",
        "Rockin' this!"
        ]

    percent = game.compute_percent_correct()
    if percent <= 30:
        fancy_print(random.choice(you_suck_message))
    if percent >= 60:
        fancy_print(blue(random.choice(you_rock_message)))


def check_if_want_quit_game(user_answer, time_start, game):
    """Encourages the user to continue playing if they ask to exit."""

    prompt = "Are you sure you want to leave? (y,n)"

    if user_answer in ["quit", "exit"]:
        while True:
            action = input(prompt).lower()
            if action in ["y", "yes"]:
                fancy_print("Ok, hope to see you soon!")
                end_game(time_start, game)
                exit(0)
            if action in ["n", "no"]:
                fancy_print("Great! Let's do some more!")
                break
            else:
                print(red("Invalid input: y or n, please!"))


def evaluate_user_answer_spelling(true_answer, user_answer, game):
    """Creates a ratio showing how close to correct the user was."""

    MIN_SPELLING_RATIO = 0.75

    how_correct_spell = SequenceMatcher(None, true_answer.lower(), user_answer.lower())
    spelling_ratio = how_correct_spell.ratio()

    if spelling_ratio >= MIN_SPELLING_RATIO:
        game.right += 1
        if spelling_ratio == 1:
            game.correct_spell += 1
        else:
            game.little_wrong_spell += 1
            print("Technically the correct spelling of %s is %s but you are close enough we'll "
                  "call it good!" %(user_answer, true_answer))
        fancy_print("Now at %d points with %d percent correct!" % (game.right,
                                                                   game.compute_percent_correct()))
    else:
        game.wrong += 1
        game.so_wrong_spell += 1
        fancy_print("Wrong! The correct answer is %s! Still %d points, now %d percent correct!"
                    % (true_answer, game.right, game.compute_percent_correct()))

    action_based_on_percent(game)
    # FIXME: Make difficulty levels that have defaults of harder min_spelling_ratios, etc.
    # and user choses their level.


def make_scoreboard():
    """Creates game scoreboard using SQLite (os talks to console, creates db file, saves, "
      "closes connection)."""
## in """ don't need quotes at the end of a line

    if not os.path.isfile('scores.db'):
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE scores
                    (name text, score integer, time unix, timer integer)""")
        conn.commit()
        conn.close()
# maybe tracking wrong answers
# store more than you might want to show
# multiple files = more crap flying around
# easier to join mulple tables in one db than multiple db's

def end_game(time_start, game):
    """Calls functions needed to end the game, stops game timer, and calculates duration of game."""

    time_end = time.time()
    time_of_game_play = (time_end - time_start)

    pretty_time = seconds_to_pretty_time(time_of_game_play)
    update_scoreboard(game, pretty_time)

    if game.current_turn > 0:
        game_summary(game, pretty_time)


def seconds_to_pretty_time(time_of_game_play):
    """Converts the calculated game duration from seconds to more easily read units."""

    secs = int(time_of_game_play)
    if secs < 60:
        return "%d s" %(secs)

    mins = secs / 60
    secs -= mins * 60 # would get diff answer with modulo b/c floats
    if mins < 60:
        return "%d h %02d m" %(mins, secs) # pads two digits with zero :00

    hours = mins / 60
    mins -= hours * 60
    if hours < 24:
        return "%d h %02d m %02d" %(hours, mins, secs)

    days = hours / 24
    hours -= days * 24
    return "%d d %02d h %02d m %02d" %(days, hours, mins, secs)

    # hot tip : give computers computer things and humans human things
    # therefore give the pretty one (at last minute) to the human and the second to the db so math and graphs etc can happen later

    # alternatively:
    # import datetime
    # str(datetime.timedelta(seconds=666))


def update_scoreboard(game, pretty_time):
    """Updates scoreboard with gamestate elements and pretty_time (seconds_to_pretty_time output)"""

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()

    # insert row of data (once per game, at end), the dot chains the function calls
    line_insert = ("INSERT INTO scores VALUES (\"%s\", %s, \"%s\", \"%s\")"
                   %(game.name, game.right, datetime.datetime.now(datetime.timezone.utc), pretty_time))

    c.execute(line_insert)
    conn.commit()
    conn.close()


def game_summary(game, pretty_time):
    """Prints summary of user results and progress."""

    MEMORIZE_THRESHOLD = 60

    print("Total points: %d" %(game.right))
    print("Percent correct: %d" %(game.compute_percent_correct()))
    print("Percent spelled correct: %d" %(game.compute_percent_spelled_correct()))
    print("Percent spelled almost correct: %d" %(game.compute_percent_spelled_almost_correct()))

    if (game.compute_percent_spelled_correct() + game.compute_percent_spelled_almost_correct()) < MEMORIZE_THRESHOLD:
        print("You spelled %d very wrong, so I expect you were typing entirely wrong answers. "
              "Better hit the flashcards again!" %(game.compute_percent_spelled_very_wrong()))

        # FIXME: Add list of words that were spelled wrong. Need to keep track with db or list.
