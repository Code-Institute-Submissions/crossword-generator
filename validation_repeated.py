from source.crossword_validator import validate
from source.constants import AnsiCommands
from source.crossword_generator import Crossword

import json
import sys


def main():
    """Main entry point for the program"""
    word_length_map = {}
    with open('data/crossword_dictionary.json', 'r',
              encoding='utf-8') as file:
        word_dict = json.load(file)

        # Build a python dictionary with word lengths as keys, and lists of
        # words of that length as values. The dictionary is used to search for
        # matching partial words
        for word in word_dict.keys():
            word = word.replace('\n', '')
            length = len(word)
            if length in word_length_map:
                word_length_map[length].append(word)
            else:
                word_length_map[length] = []
                word_length_map[length].append(word)

    iterations = 100
    for counter in range(1, iterations + 1):
        sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
        sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
        print(f"Testing number {counter}")
        crossword = Crossword(12, 12, word_length_map, word_dict,
                              user_present=False)
        result = validate(crossword)
        if result is False:
            print(f"problem at iteration {counter}")
            sys.exit()
    print(f"Tested {iterations} crosswords ... all valid")


if __name__ == '__main__':
    main()
