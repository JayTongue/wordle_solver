import json
import string
import os

alphanumeric = set(string.ascii_lowercase)
scrabble = set(word.strip() for word in open('data/scrabble-fives.txt'))

ranked = {}
for file in os.listdir('data/books'):
  for line in open(f'data/books/{file}'):
    for word in line.split():
      word = ''.join(letter for letter in word if letter in alphanumeric)
      if len(word) == 5 and word in scrabble:
        ranked[word] = ranked.get(word, 0) + 1
  json.dump(ranked, open('data/ranked.json', 'w'))

print('Done!')