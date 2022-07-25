from ast import Or
from grp import getgrgid
import random
from constants import Orientation, get_large_letter, Colors, UniChars, AnsiCommands

class Word:
    def __init__(self, orientation, string, row, col):
        self.orientation = orientation
        self.string = string
        self.start_row = row
        self.start_col = col

class Crossword:
    """Represents a crossword object"""
    def __init__(self, cols, rows, word_dict):
        self.cols = cols
        self.rows = rows
        self.grid = [["_" for i in range(rows)] for j in range(cols)]
        self.word_dict = word_dict
        self.intersections = []

        # Generate a random crossword layout
        self.generate_words()
        self.print()

    def generate_words(self):
        """This function generates the words for the crossword"""
        blank_chars = ['_' for i in range(self.cols)]
        blank_string = ''.join(blank_chars)
        print(f"{blank_string} (length = {len(blank_string)})")
        self.intersections = [(0, 2, Orientation.VERTICAL),
                              (0, 4, Orientation.VERTICAL),
                              (0, 6, Orientation.VERTICAL),
                              (0, 8, Orientation.VERTICAL),
                              (0, 10, Orientation.VERTICAL)]
        matches = find_matches(blank_string, self.word_dict)
        choice = random.choice(matches)
        self.add_word_to_grid(Word(Orientation.HORIZONTAL, choice, 0, 0))

        next_word = self._generate_new_word()
        self.add_word_to_grid(next_word)

        next_word = self._generate_new_word()
        self.add_word_to_grid(next_word)

        next_word = self._generate_new_word()
        self.add_word_to_grid(next_word)

    def _generate_new_word(self):
        """Generates one new word in the crossword, if possible"""

        # Shuffle the intersections list and pop the last one
        random.shuffle(self.intersections)
        root_cell = self.intersections.pop()
        (root_row, root_col, orientation) = root_cell
        print(f"root_row == {root_row}, root_col == {root_col}")
        potential_word = []
        potential_word.append(self.grid[root_row][root_col])
        self.print()

        if orientation == Orientation.VERTICAL:
            row = root_row + 1
            while row < self.rows:
                if self._check_cell_is_legal(row, root_col, Orientation.VERTICAL):
                    potential_word.append(self.grid[row][root_col])
                else:
                    break
                row += 1
            row = root_row - 1
            while row >= 0:
                if self._check_cell_is_legal(row, root_col, Orientation.VERTICAL):
                    potential_word.insert(0, self.grid[row][root_col])
                else: 
                    break
                row -= 1
        elif orientation == Orientation.HORIZONTAL:
            col = root_col + 1
            while col < self.cols:
                if self._check_cell_is_legal(root_row, col, Orientation.HORIZONTAL):
                    potential_word.append(self.grid[root_row][col])
                else:
                    break
                col += 1
            col = root_col - 1
            while col >= 0:
                if self._check_cell_is_legal(root_row, col, Orientation.HORIZONTAL):
                    potential_word.insert(0, self.grid[root_row][col])
                else:
                    break

        print(''.join(potential_word))
        matches = find_matches(potential_word, self.word_dict)
        choice = random.choice(matches)
        print(f"Word : orientation {orientation}, string {choice}, row {root_row}, col {root_col}")

        return Word(orientation, choice, root_row, root_col)
        

    def _check_cell_is_legal(self, row, col, orientation):
        """Checks if the cell can be used as part of a new word in the crossword"""

        # If this cell already contains a letter, it is already part of a word
        # running in the orthogonal direction, so it is a legal cell in a potential
        # new word
        if self.grid[row][col] != "_":
            print(f"cell at row {row}, col {col} is not empty")
            return True

        # If this cell is blank, then the cells neighbouring it must be blank. Otherwise, 
        # a new letter would be added at the start or end of an existing word, thereby
        # altering it.
        if orientation == Orientation.VERTICAL:
            has_cell_to_left = col > 0
            has_cell_to_right = col < self.cols - 1
            if has_cell_to_left and self.grid[row][col - 1] != "_":
                return False
            if has_cell_to_right and self.grid[row][col + 1] != "_":
                return False
        elif orientation == Orientation.HORIZONTAL:
            has_cell_above = row > 0
            has_cell_below = row < self.rows - 1
            print(f"has_cell_above == {has_cell_above}, has_cell_below == {has_cell_below}")
            if has_cell_above and self.grid[row -1][col] != "_":
                return False
            if has_cell_below and self.grid[row + 1][col] != "_":
                return False

        return True

    def _vertical_neighbour_check(self, row, col):
        """Checks if the cell can be used as part of a new word in the crossword"""

        # Assume that the cell is legal initially
        cell_is_legal = True

        # Only check neighbours if this cell is blank - adding a letter at the start
        # or end of an existing word should be avoided, as it may not result in a new legal
        # word. Running a new word through an existing word is fine, as it does not alter
        # the existing word. In fact, it's the whole point of a crossword.
        if self.grid(row, col) == "_":
            has_cell_to_left = col > 0
            has_cell_to_right = col < self.cols
            if has_cell_to_left and self.grid[row][col - 1] != "_":
                cell_is_legal = False
            if has_cell_to_right and self.grid[row][col + 1] != "_":
                cell_is_legal = False

        return cell_is_legal

    def add_word_to_grid(self, word):
        """Adds a word to the crossword grid in the correct orientation"""
        for i, value in enumerate(word.string):
            if word.orientation == Orientation.HORIZONTAL:
                self.grid[word.start_row][word.start_col + i] = word.string[i]
            else:
                self.grid[word.start_row + i][word.start_col] = word.string[i]


    def print(self):
        """Print the crossword to the terminal"""
        light_gray = Colors.get_background_color(220, 220, 220)
        dark_gray = Colors.get_background_color(0, 0, 0)
        text_color = Colors.get_foreground_color(0, 0, 0)
        print("Here's the crossword : ")
        for row in self.grid:
            display_chars = []
            for char in row:
                if char == '_':
                    display_chars.append(f"{dark_gray}{UniChars.EMPTY_SQUARE}{AnsiCommands.DEFAULT_COLOR}")
                else:
                    display_chars.append(f"{light_gray}{text_color}{get_large_letter(char)}{AnsiCommands.DEFAULT_COLOR}")
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
    if len(matches) == 0:
        error_msg = f"No words match this string : '{word}'"
        raise Exception(error_msg)
    return matches


if __name__ == '__main__':
    main()