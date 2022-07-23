import random
from constants import Orientation, get_large_letter, Colors, UniChars, AnsiCommands

class Word:
    def __init__(self, orientation, string, x, y):
        self.orientation = orientation
        self.string = string
        self.start_x = x
        self.start_y = y

class Crossword:
    """Represents a crossword object"""
    def __init__(self, cols, rows, word_dict):
        self.cols = cols
        self.rows = rows
        self.grid = [["_" for i in range(cols)] for j in range(rows)]
        self.word_dict = word_dict
        self.print()
        self.generate_words()
        self.print()

    def generate_words(self):
        """This function generates the words for the crossword"""
        start_positions = []
        blank_chars = ['_' for i in range(self.cols)]
        blank_string = ''.join(blank_chars)
        print(f"{blank_string} (length = {len(blank_string)})")
        first_word = Word(Orientation.HORIZONTAL, blank_string, 0, 0)
        matches = find_matches(first_word.string, self.word_dict)
        choice = random.choice(matches)
        print(choice)
        self.add_word_to_grid(Word(Orientation.HORIZONTAL, choice, 0, 0))

    def add_word_to_grid(self, word):
        """Adds a word to the crossword grid in the correct orientation"""
        for i in range(len(word.string)):
            if word.orientation == Orientation.HORIZONTAL:
                self.grid[word.start_x + i][word.start_y] = word.string[i]
            else:
                self.grid[word.start_x][word.start_y + i] = word.string[i]



    def print(self):
        """Print the crossword to the terminal"""
        light_gray = Colors.get_background_color(220, 220, 220)
        dark_gray = Colors.get_background_color(0, 0, 0)
        text_color = Colors.get_foreground_color(0, 0, 0)
        print()
        print("Here's the crossword : ")
        for row in self.grid:
            display_chars = []
            for char in row:
                if char == '_':
                    display_chars.append(f"{dark_gray}{UniChars.EMPTY_SQUARE}{AnsiCommands.DEFAULT_COLOR}")
                else:
                    display_chars.append(f"{light_gray}{text_color}{get_large_letter(char)}")
            string = ''.join(display_chars)
            print(string)
        

def main():
    """Main entry point for the program"""
    word_dict = {}
    with open('data/large_dict_words_only.txt', 'r') as file:
        for word in file:
            word = word.replace('\n', '')
            length = len(word)
            if length in word_dict.keys():
                word_dict[length].append(word)
            else:
                word_dict[length] = []
                word_dict[length].append(word)
    for key, value in word_dict.items():
        print(f"Number of {key}-letter words is {len(value)}")
    crossword = Crossword(11, 11, word_dict)

def find_matches(word, word_dict):
    """Searches the word_dict to find matches for the supplied word"""
    known_chars = []
    for i, char in enumerate(word):
        if char != '_':
            known_chars.append((i, char))
    potential_matches = word_dict[len(word)]
    matches = []
    for potential_match in potential_matches:
        match = True
        for char_tuple in known_chars:
            index, char = char_tuple
            if potential_match[index] != char:
                match = False
        if match:
            matches.append(potential_match)
    return matches


if __name__ == '__main__':
    main()