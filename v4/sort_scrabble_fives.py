# sort_scrabble_fives.py

""" 
This list gets sorted according to letter scores
https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
 	
E 56.88 	
A 43.31 	
R 38.64 	
I 38.45 	
O 36.51 	
T 35.43 	
N 33.92 	
S 29.23 	
L 27.98 	
C 23.13 	
U 18.51 	
D 17.25 	
P 16.14 	
M 15.36
H 15.31
G 12.59
B 10.56
F 9.24
Y 9.06
W 6.57
K 5.61
V 5.13
X 1.48
Z 1.39
J 1.00
Q 1.00

"""
from collections import OrderedDict
import re

def main():
  infile, outfile = set_up()
  sorted_list = evaluate_word_scores(infile)
  sortier_list = evaluate_exclusion_scores(sorted_list, outfile)
  process_sorted_list(outfile, sortier_list)


def set_up():
  infile = open('tables_and_files/scrabble_fives.txt', 'r')
  outfile = open('tables_and_files/scrabble_fives_sorted.txt', 'w', encoding = 'utf-8')

  return infile, outfile


def evaluate_word_scores(infile):
  print('online!')
  sorting_list = {}
  outline_counter = 0
  for line in infile:
    line = line.strip()
    exclude_redundant_letters = []
    
    line_score = 0.0
    
    for letter in line:
      already = False
      exclude_redundant_letters.append(letter)
      for already_letter in exclude_redundant_letters[0:len(exclude_redundant_letters)-1]:
        if letter == already_letter:
          already = True
      if already == False:
        letter_score = float(score_letters(letter))
      if already == True:
        letter_score = 0.0
  
      line_score += letter_score
      line_score = round(line_score, 2)
    sorting_list[line] = line_score
    outline_counter += 1
  
  # print('sorting_list = ', len(sorting_list))
  sorted_list = dict(sorted(sorting_list.items(), key=lambda item: item[1], reverse = True))
  # sorted_list = OrderedDict(sorted(sorting_list.items()))
  # sorted_list = OrderedDict(sorted(sorting_list.items(), reverse = True))
  # print(sorted_list)

  # print('sorted_line = ',len(sorted_list))
  print('outline_counter = ',outline_counter)
  return sorted_list
  

def process_sorted_list(outfile, sorted_list):
  # print(sorted_list)
  sorted_list = str(sorted_list)
  stripped_list = re.findall(r'[a-z]+', sorted_list)

  print('stripped_list = ',len(stripped_list))
  for sorted_word in stripped_list:
    print(sorted_word, file = outfile)
    

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


def evaluate_exclusion_scores(sorted_list, outfile):
  sortier_list = {}
  for target_word in sorted_list:
    exclusion_counter = 0
    for target_letter in target_word:
      match = False
      for compare_word in sorted_list:
        for compare_letter in compare_word:
          if target_letter == compare_letter:
            match = True
      if match == True:
        exclusion_counter += 1
    sortier_list[target_word] = exclusion_counter
  print(sortier_list)

  return sortier_list


main()
        