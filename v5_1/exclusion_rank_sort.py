# sort_scrabble_fives.py

""" 
This list gets sorted according to letter scores
https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html

"""
from collections import OrderedDict
import re

def main():
  infile_1 = process_infile()
  sorted_list = calculate_score(infile_1)
  export_list(sorted_list)


def process_infile():
  infile_1 = open('tables_and_files/long_list.txt', 'r')
  
  return infile_1


def calculate_score(infile_1):
  sorting_list = {}
  for line in infile_1:
    line = line.strip()
    exclusion_score = calculate_exclusion_score(line)
    print(line, exclusion_score)
    sorting_list[line] = exclusion_score
  sorted_list = dict(sorted(sorting_list.items(), key=lambda item: item[1], reverse = True))
  print(sorted_list)

  return sorted_list


def calculate_exclusion_score(line):
  
  exclusion_score = 0
  
  infile_2 = open('tables_and_files/long_list.txt', 'r')
  for compare_word in infile_2:
    compare_word = compare_word.strip()
    match = False
    for target_letter in line:
      
      for compare_letter in compare_word:
        if target_letter == compare_letter:
          match = True
    if match == True:
      exclusion_score += 1
  
  return exclusion_score


def export_list(sorted_list):
  outfile = open('scrabble_exclusive.txt', 'w', encoding = 'utf-8')
  
  sorted_list = str(sorted_list)
  stripped_list = re.findall(r'[a-z]+', sorted_list)

  print('stripped_list = ',len(stripped_list))
  for sorted_word in stripped_list:
    print(sorted_word, file = outfile)
    

  print(stripped_list)


main()