# 5_letter_finder.py
'''
This program takes a list of words and writes 5-letter words into a separate .txt.
'''

def main():
  infile = open('dictionary.txt')
  output_file_name = f'scrabble_fives.txt'
  outfile_path_and_filename = f'{output_file_name}'
  outfile = open(outfile_path_and_filename, 'w', encoding='utf-8')
  
  for line in infile:
    line = line.strip()
    if len(line) == 5:
      line = line.lower()
      print(line, file = outfile)


main()
  