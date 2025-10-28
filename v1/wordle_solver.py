# wordle_solver.py

"""
This was an early attempt at a wordle solver using the Scramble function from my Anagram solver. 

See wordle_solver_2.py for the working version.
"""


import itertools


def main():
  words, letters, added_characters = solicit_input()
  iterations = scramble_input(words, letters, added_characters)
  combined_words_list = recombine_input(iterations)
  check_against_word_list(combined_words_list)


def solicit_input():
  # solicits input and splits into strings
  words = str(input('Enter a word to find its anagrams: '))
  if len(words) < 5:
    added_characters = 5 - len(words)
  letters = list(words)
  print(f'\nYour characters are: {letters}')
  print(f'I need to add {added_characters} to get to 5 characters.')
  return words, letters, added_characters
  
  
def scramble_input(words, letters, added_characters):
   # Takes letters and scrambles them
  x = len(words)
  print(f'\nYou have {x} characters in your input.')
  iterations = []
  all_letters_list= ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
  while x > 0:
    iterations += list(itertools.permutations(letters, x))
    x = x-1
  return iterations


def recombine_input(iterations):
   # recombine
  combined_words_list = []
  for iter in iterations:
      newWord = ""
      for letter in iter:
          newWord += letter
      combined_words_list.append(newWord)
  print()
  print('Here are your permutations:')
  print(combined_words_list)
  return combined_words_list

def check_against_word_list(combined_words_list):
  # checks against word list  
  print('\nHere are your anagrams:')
  infile = open('corncob_lowercase.txt')
  for word in combined_words_list:
    word = str(word)
    word = word.lower()
    # print(f'matching word: {word}')
    for line in infile:
      line = str(line)
      line = line.strip()
      line = line.lower()
      # print(line)
      if word == line:
        print(word)
        # print(f'match found: {word}')
    infile.seek(0)
  print('That\'s all!')
  infile.close()

        
main()