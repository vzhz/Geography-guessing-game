"""Core functionality for flashcard game."""

# python std library
import datetime
from difflib import SequenceMatcher
import os
import sqlite3
import sys
import time

# libraries
from curtsies.fmtfuncs import red, bold, blue

# my code
from gamestate import Mode



def check_version():
    """Tests if Python version is 3.5.x and print user instructions if it is not."""

    message = (
        "Hey asshole, did you even read the README? You're using the wrong Python "
        "version and are going to be very sad when I don't save your score."
    )
    prompt = "Would you like to leave and restart after opening with the correct version [y,n]?:"

    if not (sys.version_info[0] == 3 and sys.version_info[1] == 5):
        print(red(message))
        if input(prompt).lower() in ["y", "yes"]:
            print(bold("Remember to type 'Python3'"))
            exit()


def fancy_print(string, i=1):
    """Adds i extra lines after printed message."""

    print(string + "\n" * i)


def state_capital_pairs():
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
        ).lower()

    if user_input == "1":
        return QuestionFile.us_state_capital
    if user_input == "2":
        return QuestionFile.french_food
    if user_input == "3":
        return QuestionFile.metric
    if user_input == "4":
        return QuestionFile.multiplication
    if user_input == "5":
        return QuestionFile.user

    print("Learn to type, punk.\n")

    # FIXME: use a dictionary for constant time lookups.
    pairs = []

    with open(user_file_name, 'r') as f:
        for line in f.read().splitlines():
            pairs.append(tuple(line.split(',')))
    print(pairs)
    print(len(pairs))
    return pairs


def ask_mode():
    """Asks user if s/he would like to respond with the first or second element of the pair
       when given the other."""

    #FIXME: Gives 3rd option when 1st option is requested.

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
            return Mode.capital
        if user_input == "2":
            return Mode.state
        if user_input == "3":
            return Mode.random

        print("Learn to type, punk.\n")


def ask_turns_goal():
    """Asks user how many turns they plan to do."""

    turns_goal = int(input("How many turns would you like to do today? \n"))
    return turns_goal


def asks_user_question(game):
    """Gives user one side of the pair and asks them to type other side of the pair."""

    state, capital = game.get_state_capital_pair()

    if game.mode == Mode.capital:
        user_answer = input("What is the capital of %s? " % state)
        return user_answer, capital
    elif game.mode == Mode.state:
        user_answer = input("What state has the capital %s? " % capital)
        return user_answer, state


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
        "C'on, human.",
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


def judge_spelling(true_answer, user_answer, game):
    """Creates a ratio showing how close to correct the user was."""

    min_spelling_ratio = 0.75

    how_correct_spell = SequenceMatcher(None, true_answer.lower(), user_answer.lower())
    spelling_ratio = how_correct_spell.ratio()

    if spelling_ratio >= min_spelling_ratio:
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

    if os.path.isfile('scores.db'):
        pass
    else:
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE scores
                    (name text, score integer, time unix, timer integer)""")
        conn.commit()
        conn.close()


def end_game(time_start, game):
    time_end = time.time() #end game timer
    time_of_game_play = (time_end - time_start) #in seconds
    pretty_time = seconds_to_pretty_time(time_of_game_play)
    update_scoreboard(game, pretty_time)
    #game_summary(game, pretty_time_of_game_play)  MECHANGE
    if game.current_turn > 0:
        game_summary(game, pretty_time)

def seconds_to_pretty_time(time_of_game_play):
    #time_of_game_play is in secs
    secs = int(time_of_game_play)
    #print(secs)
    if secs < 60:
        #print("%d s" %(secs))
        return "%d s" %(secs)
    mins = secs / 60
    secs -= mins * 60 #note: might get diff answer with modulo is using floats but this is an int, yay!
    if mins < 60:
        return "%d h %02d m" %(mins, secs) #pads two digits with zero :00
    hours = mins / 60
    mins -= hours * 60
    if hours < 24:
        return "%d h %02d m %02d" %(hours, mins, secs)
    days = hours / 24
    hours -= days * 24
    return "%d d %02d h %02d m %02d" %(days, hours, mins, secs)
    #alternatively:
    #import datetime
    #str(datetime.timedelta(seconds=666))

def update_scoreboard(game, pretty_time):
    """pretty_time is an output from seconds_to_pretty_time"""
    #ask for users name

    name = input("What be your flashcard-masterin' name, you little badass?")
    #connect
    conn = sqlite3.connect('scores.db')
    #cursor
    c = conn.cursor()
    #insert row of data (once per game, at end), the dot chains the function calls
    blob = ("INSERT INTO scores VALUES (\"%s\", %s, \"%s\", \"%s\")" %(name, game.right, datetime.datetime.now(datetime.timezone.utc), pretty_time))
    #print(blob)
    c.execute(blob) #pass parm. in at exe, look at tutorial, see sql query not string
    #c.execute("INSERT INTO scores VALUES (%s, %s, %s, %s)" %(name, game.right, datetime.datetime.now(datetime.timezone.utc), pretty_time_of_game_play))\
                                        #({name}, {score}game.right, {timestamp}datetime.datetime.now(datetime.timezone.utc), \
                                        #{duration}pretty_time_of_game_play")
    #save row just added
    conn.commit()
    #close connection
    conn.close()

def game_summary(game, pretty_time_of_game_play):
#should I ask user how mean we should be re: spelling before we decide they weren't spelling the right word at all?
#maybe we should have difficulty levels
    MEMORIZE_THRESHOLD = 60

    print("Total points: %d" %(game.right))
    print("Percent correct: %d" %(game.compute_percent_correct()))
    print("Percent spelled correct: %d" %(game.compute_percent_spelled_correct()))
    print("Percent spelled almost correct: %d" %(game.compute_percent_spelled_almost_correct()))
    #communicate with whitespace
    if (game.compute_percent_spelled_correct() + game.compute_percent_spelled_almost_correct()) < MEMORIZE_THRESHOLD:
        print("You spelled %d very wrong, so I expect you were typing entirely wrong answers. Better hit the flashcards again!" %(game.compute_percent_spelled_very_wrong()))
