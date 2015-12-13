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
    # Prints out a string with i newlines after it
    print(string)
    print("\n"*i) #use fancy_print instead of print

def state_capital_pairs():
    state_capital_pairs = []
    with open('state_capitals.txt', 'r') as f: #make generic
        splitlines = f.read().splitlines()
        for line in splitlines:
            state, capital = line.split(',')
            state_capital_pairs.append((state, capital))
    return state_capital_pairs
    # later, list comp

def ask_mode():
    while True:
        user_input = input(
            "\nWould you like to guess capitals given states or vice versa?"
            "\n"
            "\n  1: If you want to guess capitals given states."
            "\n  2: If you want to guess states given capitals."
            "\n  3: If you want a mix of both!"
            "\n"
            "\ntype your choice [1,2,3]: "
        ).lower()
        if user_input == "1":
            return Mode.capital
        if user_input == "2":
            return Mode.state
        if user_input == "3":
            return Mode.random
        print("Learn to type, punk. \n")

def ask_turns_goal():
    while True:
        turns_goal = int(input("How many turns would you like to do today? \n"))
        fancy_print(blue("%d is a great number of rounds! Go you! \n" % turns_goal))
        return turns_goal

# def ask_repeat_questions():
#   while True:
#       repeat_questions = (input("Type 'repeat' and enter if you want to see state/capital pairs more than \n \
#           once, and enter if want to see state/capital pairs only once \n"))
#       return repeat_questions

def asks_user_question(game): #could put asking and checking into same function
    (state, capital) = game.get_state_capital_pair()
    if len(game.get_state_capital_pair()) > 0:
        if game.mode == Mode.capital:
            user_answer = input("What is the capital of %s? \n" % state) #have user add input when they load a new file
            return user_answer, capital
        if game.mode == Mode.state:
            user_answer = input("What state has the capital %s? \n" % capital) #same as above
            return user_answer, state
    else:
        pass

def action_based_on_turns(game):
    if game.current_turn == game.turns_goal-game.turns_goal / 10 and game.current_turn > 1:
        print(blue("Almost to your rounds goal! Finallll pushhhh!"))#should this be a return statement?
    if game.current_turn == game.turns_goal+1:
        print("Would you like to continue? Practice makes perfect! Type 'quit' if you ever want to exit.")
    if game.current_turn == game.turns_goal/10 or game.current_turn == game.turns_goal / 5:
        print(blue("You're doing a great job, keep going!"))
    if game.current_turn == 60:
        return "Really, you should stop.  It's bedtime. Type 'quit' anytime to exit. Or continue, because you \
        really really want to learn these state capitals."

def action_based_on_percent(game):
    percent = game.compute_percent_correct()
    if percent <= 30:
        fancy_print("Keep trying! You'll get it!")
    if percent >= 60:
        fancy_print(blue("You're doing awesomely! Are you *sure* you weren't on Quiz Bowl in highschool?"))

def check_if_want_quit_game(user_answer, time_start, game):
    if user_answer == "quit" or user_answer == "exit":
        user_wants_to_stay = input("Are you sure you want to leave? (y,n)") #boolean would make sense if were asking Y/N more than once
        while True:
            if user_wants_to_stay.lower() == "y" or user_wants_to_stay.lower() == "yes":
                fancy_print("Ok, hope to see you soon!")
                end_game(time_start, game)
                exit(0)
            if user_wants_to_stay.lower() == "n" or user_wants_to_stay.lower() == "no":
                fancy_print("Great! Let's do some more!")
                break
            else:
                user_wants_to_stay = input("Please choose 'y' to leave or 'n' to stay")
                continue
    #maybe test user answer fcn
    #if user_answer == true_answer.lower():

def judge_spelling(true_answer, user_answer, game):
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
            print ("The correct spelling is %s but your spelling is so close! We'll call it good!" %true_answer)
        fancy_print(blue("Yay, you got points! Now at %d points with %d percent correct!" %(game.right, game.compute_percent_correct())))
    else:
        game.wrong += 1
        game.so_wrong_spell += 1
        fancy_print("Wrong! The correct answer is %s! Still %d points, now %d percent correct!" %(true_answer, game.right, game.compute_percent_correct()))
    action_based_on_percent(game)

###end game
def make_scoreboard():
    if os.path.isfile('scores.db'): #os talks to console
        pass
    else:
        #create db file for scores
        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE scores
                    (name text, score integer, time unix, timer integer)""") #local variable, not access outside
        #save your changes!
        conn.commit()
        #done with connection for now
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
