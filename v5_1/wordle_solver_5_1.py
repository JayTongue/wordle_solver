# wordle_solver_2.py
'''
This program is the functioning verion of the wordle solver.

(for Luke, if you ever see this:

Ideas for future dev:
  The wordle bot by NYT will guess a first strong guess, then adjust subsequent guesses. I think the 'generate optimal guesses' could be adapted/evolved to do this. Perhaps taking the optimal guesses and favoring them by internal non-repetition as well as common vs uncommon letters?
  The idea is to eventually come up with a program that can consistently get the number of guesses it can, and ideally also beat the NYT wordle bot.)
  
'''

import re

def main():
  introduce()
  replay_answer = True
  while replay_answer == True:
    infile = set_up()
    greens, yellows, blacks = solicit_inputs()
    black_results, yellows = cut_word_list(infile, greens, yellows, blacks)
    generate_optimal_guesses(infile, greens, yellows, blacks, black_results)
    replay_answer = replay()
  clean_up(infile)


def introduce():
  print()
  print('Hello! Welcome to Justin\'s Wordle Solver.\n')
  print('This program uses the 2015 Scrabble Dictionary.\n')
  print('Here\'s the Wordle Website: https://www.nytimes.com/games/wordle/index.html \n')
  print('These are suggested first guesses:\n\'STERN\'\n\'YCLAD\'\n\'WHOMP\'')
  print()
  print('Here is the format for inputing greens and yellows: [LETTER][POSITION] then press <ENTER>. Press <ENTER> when done.')
  print('For instance: \na1 \nb2\nc3')
  print('Blacks will not have a position, just a letter.')


def set_up():
  infile = open(f'tables_and_files/short_list_sorted.txt')
  return infile


def solicit_inputs():
  greens = []
  print(f'\nTell me your current guesses:\n')
  print(f'greens:')
 
  while True:
    green = input()
    if green != '':
      greens.append(green)
    else: break
  print(f'Here are your greens: {greens}\n')

  yellows = []
  print(f'yellows:')
  while True:
    yellow = input()
    if yellow != '':
      yellows.append(yellow)
    else: break
  print(f'Here are your yellows: {yellows}\n')

  blacks = []
  print(f'blacks:')
  while True:
    black = input()
    if black != '':
      blacks.append(black)
    else: break
  print(f'Here are your blacks: {blacks}\n')

  return greens, yellows, blacks


def cut_word_list(infile, greens, yellows, blacks):
  green_results = process_greens(infile, greens)
  yellow_results = process_yellows(yellows, green_results)
  black_results = process_blacks(blacks, yellow_results)
  infile.close()

  return black_results, yellows


def process_greens(infile, greens):
  green_results = []

  for line in infile:
    line = line.strip()
    match = True
    for green in greens:
      letter = green[0]
      position = int(green[1])
      position = position - 1
      if line[position] != letter:
        match = False
    if match == True:
      green_results.append(line)
  # print(f'Here are your possiblities considering greens \n{green_results}\n')
  print(f'Applying Green parameters yeilds {len(green_results)} possibilities.\n')
  return green_results


def process_yellows(yellows, green_results):
  yellow_results = []

  for line in green_results:
    match = True
    letter_accumulator = 0
    
    for yellow in yellows:
      letter = yellow[0]
      position = int(yellow[1])
      position = position - 1
      if line[position] == letter:
        match = False 
        #This flips to False if a yellow letter is where it shows yellow.
        
      line_bool = False #This flips to True if the letter appears in ANOTHER PLACE
      for line_letter in line:
        if line_letter == letter:
          line_bool = True
      if line_bool == True:
        letter_accumulator += 1
    # print(int(letter_accumulator), int(len(yellows)))
    if match == True and int(letter_accumulator) == int(len(yellows)):
      yellow_results.append(line)
  # print(f'Here are your possibilities considering yellows \n{yellow_results}\n')
  print(f'Applying Green and Yellow Parameters yeilds {len(yellow_results)} possibilities.\n')
  return yellow_results


def process_blacks(blacks, yellow_results):
  black_results = []

  for black_letter_line in yellow_results:
    black_match = True
    for black in blacks:
      for black_line_letter in black_letter_line:
        if black == black_line_letter:
          black_match = False
    if black_match == True:
      black_results.append(black_letter_line)

  print(f'Applying Green, Yellow, and Black parameters yeilds {len(black_results)} possibilities:')
  print(f' \n{black_results}\n')

  return black_results



def generate_optimal_guesses(infile, greens, yellows, blacks, black_results):

  yellow_guesses = []

  infile = open('tables_and_files/long_list_sorted.txt', 'r')
  for line in infile:
    line = line.strip()
    yellow_match = True
    letter_accumulator = 0
    
    for yellow in yellows:
      letter = yellow[0]
      position = int(yellow[1])
      position = position - 1
      if line[position] == letter:
        yellow_match = False 
        #This flips to False if a yellow letter is where it shows yellow.
        
      line_bool = False #This flips to True if the letter appears in ANOTHER PLACE
      for line_letter in line:
        if line_letter == letter:
          line_bool = True
      if line_bool == True:
        letter_accumulator += 1
    # print(int(letter_accumulator), int(len(yellows)))
    if yellow_match == True and int(letter_accumulator) == int(len(yellows)):
      yellow_guesses.append(line)

  black_guesses = []

  for black_letter_line in yellow_guesses:
    black_match = True
    for black in blacks:
      for black_line_letter in black_letter_line:
        if black == black_line_letter:
          black_match = False
    if black_match == True:
      black_guesses.append(black_letter_line)

  all_known = []
  all_known.append(greens)
  all_known.append(yellows)
  all_known.append(blacks)
  all_known = str(all_known)
  all_known_list = re.findall(r'[a-z]', all_known, re.IGNORECASE)

  sorted_list = evaluate_word_scores(all_known_list, black_guesses)
  process_sorted_list(sorted_list)


def evaluate_word_scores(all_known_list, black_guesses):
  print('online!')
  sorting_list = {}
  outline_counter = 0
  for word in black_guesses:
    word = word.strip()
    exclude_redundant_letters = []
    
    line_score = 0.0
    
    for letter in word:
      already = False
      exclude_redundant_letters.append(letter)
      for already_letter in exclude_redundant_letters[0:len(exclude_redundant_letters)-1]:
        if letter == already_letter:
          already = True
        for known_letter in all_known_list:
          if letter == known_letter:
            already = True
      if already == False:
        letter_score = float(score_letters(letter))
      if already == True:
        letter_score = 0.0
  
      line_score += letter_score
      line_score = round(line_score, 2)
    sorting_list[word] = line_score
    outline_counter += 1
  
  # print('sorting_list = ', len(sorting_list))
  sorted_list = dict(sorted(sorting_list.items(), key=lambda item: item[1], reverse = True))
  # sorted_list = OrderedDict(sorted(sorting_list.items()))
  # sorted_list = OrderedDict(sorted(sorting_list.items(), reverse = True))
  # print(sorted_list)

  # print('sorted_line = ',len(sorted_list))
  print('outline_counter = ',outline_counter)
  return sorted_list
  

def process_sorted_list(sorted_list):
  # print(sorted_list)
  sorted_list = str(sorted_list)
  stripped_list = re.findall(r'[a-z]+', sorted_list)

  print('stripped_list = ',len(stripped_list))

  print(stripped_list)


def score_letters(letter):
  if letter == 'e':
    letter_score = 56.88 	
  elif letter == 'a':
    letter_score = 43.31 	
  elif letter == 'r': 
    letter_score = 38.64 	
  elif letter == 'i':
    letter_score = 38.45 	
  elif letter == 'o':
    letter_score = 36.51 	
  elif letter == 't':
    letter_score = 35.43 	
  elif letter == 'n':
    letter_score = 33.92 	
  elif letter == 's':
    letter_score = 29.23 	
  elif letter == 'l':
    letter_score = 27.98 	
  elif letter == 'c':
    letter_score = 23.13
  elif letter == 'u':
    letter_score = 18.51 	
  elif letter == 'd':
    letter_score = 17.25 	
  elif letter == 'p':
    letter_score = 16.14 	
  elif letter == 'm': 
    letter_score = 15.36
  elif letter == 'h':
    letter_score = 15.31
  elif letter == 'g': 
    letter_score = 12.59
  elif letter == 'b': 
    letter_score = 10.56
  elif letter == 'f':
    letter_score = 9.24
  elif letter == 'y':
    letter_score = 9.06
  elif letter == 'w':
    letter_score = 6.57
  elif letter == 'k':
    letter_score = 5.61
  elif letter == 'v':
    letter_score = 5.13
  elif letter == 'x':
    letter_score = 1.48
  elif letter == 'z':
    letter_score = 1.39
  elif letter == 'j':
    letter_score = 1.00
  else: #if letter == 'q'
    letter_score = 1.00

  return letter_score

  

def replay():
  replay = True
  replay_reply = input('Press <ENTER> to play again. Press any other key to quit.')
  if replay_reply != '':
    replay = False
  if replay_reply == '':
    print('\n------------------------------------------------------------')
  return replay
  

def clean_up(infile):
  print('Thank you for using the Wordle Solver.\n Have a nice day!')
  infile.close()


main()