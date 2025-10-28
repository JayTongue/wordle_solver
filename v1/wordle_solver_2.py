# wordle_solver_2.py
'''
This program is the functioning verion of the wordle solver.

(for Luke, if you ever see this:

Ideas for future dev:
  The wordle bot by NYT will guess a first strong guess, then adjust subsequent guesses. I think the 'generate optimal guesses' could be adapted/evolved to do this. Perhaps taking the optimal guesses and favoring them by internal non-repetition as well as common vs uncommon letters?
  The idea is to eventually come up with a program that can consistently get the number of guesses it can, and ideally also beat the NYT wordle bot.)
  
'''

def main():
  introduce()
  replay_answer = True
  while replay_answer == True:
    infile = set_up()
    greens, yellows, blacks = solicit_inputs()
    cut_word_list(infile, greens, yellows, blacks)
    generate_optimal_guesses(infile, greens, yellows, blacks)
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
  infile = open(f'scrabble_fives.txt')
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
  process_blacks(blacks, yellow_results)
  infile.close()


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


def generate_optimal_guesses(infile, greens, yellows, blacks):
  ask_guesses = input('Don\'t know what to guess? Would you like optimal guesses? Type [yes/no]: ')

  if ask_guesses == 'yes':
    print('Here are some optimal guesses that only have letters you have NO data on:')
    
    optimal_guesses = []
    infile = open(f'scrabble_fives.txt')
    for line in infile:
      line = line.strip()
      unmatched = True
      for infile_letter in line:
        for green_word in greens:
          green_letter = green_word[0]
          if green_letter == infile_letter:
            unmatched = False
        for yellow_word in yellows:
          yellow_letter = yellow_word[0]
          if yellow_letter == infile_letter:
            unmatched = False
        for black_word in blacks:
          if black_word == infile_letter:
            unmatched = False
      if unmatched == True:
        optimal_guesses.append(line)
    if not optimal_guesses:
      print('Unfortunately, there are no optimal guesses\n')
    else:
      print(optimal_guesses)
      print()
  

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