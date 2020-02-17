"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    true_list = [ paragraphs[x] for x in range(len(paragraphs)) if select(paragraphs[x])==True]
    if k > len(true_list)-1:
        return ''
    else:
        return true_list[k]

    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check_topic(s):
        cleared_list = split(remove_punctuation(s.lower()))
        for x in range(len(topic)):
            if topic[x] in cleared_list:
                return True
        return False

    return check_topic
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    min_length = min(len(typed_words),  len(reference_words))
    
    if min_length == 0:
        return 0.0
    
    correct_count = 0
    for index in range(min_length):
        if typed_words[index] == reference_words[index]:
             correct_count += 1

    return (correct_count/len(typed_words)) * 100
                
        
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return (len(typed)/5)/(elapsed/60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than or equal to LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    if user_word in valid_words:
        return user_word
    
    diff_of_words = {}
    
    for x in range(len(valid_words)):
        diff = diff_function(user_word, valid_words[x], limit)
        if x == 0:
            diff_of_words[diff] = valid_words[x]
        if min(diff_of_words.keys()) > diff:
            diff_of_words = {diff: valid_words[x]}
    
    if min(diff_of_words.keys()) > limit:
        return user_word
    else:
        return diff_of_words.get(min(diff_of_words.keys()))
        
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(index, changes):
        if changes > limit:
            return 0
        if index == len(start):
            return 0
        if start[index] != goal[index]:
            return 1 + helper(index+1, changes+1)
        else:
            return helper(index+1, changes)

    if len(start) < len(goal):
        return (len(goal) - len(start)) + swap_diff(start, goal[0:len(start)], limit)
    elif len(start) > len(goal):
        return (len(start) - len(goal)) + swap_diff(start[0:len(goal)], goal, limit)
    else:
        return helper(0, 0)

    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""

    if start == goal or len(start) == 0 or len(goal) == 0 or limit == 0: 
        # BEGIN
        return swap_diff(start, goal, limit)
        # END

    elif start[0] == goal[0]: 
        # BEGIN
        "*** YOUR CODE HERE ***"
        return edit_diff(start[1:], goal[1:], limit)
        # END
        

    else:
        add_diff =  1 + edit_diff(goal[0]+start, goal, limit-1)
        remove_diff =  1 + edit_diff(start[1:len(start)], goal, limit - 1)
        substitute_diff = 1 + edit_diff(goal[0]+start[1:], goal, limit-1)
        # BEGIN
        "*** YOUR CODE HERE ***"
    return min(add_diff, remove_diff, substitute_diff)
        # END


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    correct_count = 0
    
    for x in range(len(typed)):
        if typed[x] == prompt[x]:
            correct_count += 1
        else:
            break
        
    progress = correct_count / len(prompt)
    send({'id': id ,  'progress': progress })
    
    return progress
    
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    '''
    words_index = 1
    retVal = [[] for i in range(n_players)]
    while words_index < n_words + 1:
        min_time = elapsed_time(word_times[0][words_index]) - elapsed_time(word_times[0][words_index-1])
        min_player_index = 0
        players_index = 1
        
        while players_index < n_players:
            if elapsed_time(word_times[players_index][words_index]) - elapsed_time(word_times[players_index][words_index-1]) < min_time:
                min_time = elapsed_time(word_times[players_index][words_index]) - elapsed_time(word_times[players_index][words_index-1]) 
                min_index = players_index
            players_index += 1

        
        players_index = 0
        
        while players_index < n_players:
            if abs(elapsed_time(word_times[players_index][words_index]) - elapsed_time(word_times[players_index][words_index-1]) - min_time) < margin:
                retVal[players_index].append(word(word_times[players_index][words_index]))
            players_index += 1
            
        words_index += 1
    return retVal
    '''
    def create_player_list(player):
        time_list = []
        for x in range(1, len(player)):
            time_list.append(elapsed_time(player[x])-elapsed_time(player[x-1]))
        return time_list

    player_time_list = []
    for x in range(len(word_times)):
        player_time_list.append(create_player_list(word_times[x]))

    word_list = []
    for x in range(1, len(word_times[0])):
        word_list.append(word(word_times[0][x]))


    min_list = []
    for y in range (len(word_list)):
        minimum = player_time_list[0][y]
        for x in range(len(player_time_list)):
            if player_time_list[x][y] < minimum :
                minimum = player_time_list[x][y]
        min_list.append(minimum)

    fastest_list = [[] for i in range(len(player_time_list))]
    for y in range(len(word_list)):
        for x in range( len(player_time_list)):
            if player_time_list[x][y] - min_list[y] < margin:
                fastest_list[x].append(word_list[y])

    return fastest_list
                
  
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
