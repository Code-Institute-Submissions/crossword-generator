import json
from crossword_generator import Crossword

def main():
    """Main entry point for the program"""
    dict_by_length = {}
    with open('data/crossword_dictionary.json', 'r', encoding='utf-8') as file:
        word_dict = json.load(file)
        for word in word_dict.keys():
            word = word.replace('\n', '')
            length = len(word)
            if length in dict_by_length:
                dict_by_length[length].append(word)
            else:
                dict_by_length[length] = []
                dict_by_length[length].append(word)
    crossword = Crossword(11, 11, dict_by_length, word_dict)

    beginPuzzle(crossword)

def beginPuzzle(crossword):
    pass

if __name__ == '__main__':
    main()