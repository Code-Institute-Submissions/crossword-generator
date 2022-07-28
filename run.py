import random
import json
from constants import Orientation, get_large_letter, Colors, AnsiCommands

class Word:
    """Represents a word in the crossword puzzle. Specifies the word string, 
       the starting row and column, and the orientation (down or across)"""
    def __init__(self, orientation, string, row, col):
        self.orientation = orientation
        self.string = string
        self.start_row = row
        self.start_col = col

class Clue:
    """Represents a clue for a given word - specifies the start location of the word, 
       the orientation (down or across), the ordinal number of this clue, and a list
       containing at least one definition"""
    def __init__(self, string, index, orientation, definitions, start_row, start_col):
        self.string = string
        self.index = index
        self.orientation = orientation
        self.definitions = definitions
        self.start_row = start_row
        self.start_col = start_col

    def __str__(self):
        output = f"{self.string} : {self.index} {self.orientation.value}\n{self.definitions}"
        return output

class Crossword:
    """Represents a crossword object"""
    def __init__(self, rows, cols, dict_by_length, word_dict):
        self.cols = cols
        self.rows = rows
        self.grid = [["_" for i in range(rows)] for j in range(cols)]
        self.word_dict = word_dict
        self.dict_by_length = dict_by_length
        self.clues = []

        # A set is used to prevent duplicate intersections
        self.intersections = set() 
        
        # Generate a random crossword layout
        self.generate_words()
        self.print()

    def generate_words(self):
        """This function generates the words for the crossword"""

        # Create the initial blank string for the first word in the crossword, 
        # choosing a string oriented across of random length.
        blank_chars = ['_' for i in range(random.randint(3, self.cols - 1))]
        blank_string = ''.join(blank_chars)
        
        # Find words matching this initial string, and add it to a random row.
        matches = find_matches(blank_string, self.dict_by_length, self.word_dict)
        choice = matches[0]
        random_row = random.randint(0, self.rows - 1)
        first_word = Word(Orientation.HORIZONTAL, choice, random_row, 0)
        self.add_word_to_grid(first_word)
        self.add_word_to_clues(first_word)
        
        self.print()
        # Loop that generates all subsequent words
        while len(self.intersections) > 0:
            # Print the intersections_list to the terminal
            next_word = self._generate_new_word()
            if next_word is not None:
                self.add_word_to_grid(next_word)
                self.add_word_to_clues(next_word)
                self.print()
                self._prune_intersection_set()
                # self._print_intersections()
                # input("Press enter to continue")
                print('---------------------------------------------------------')
        for clue in self.clues:
            print()
            print(clue)

    def add_word_to_clues(self, word):
        """Derive a clue from the word provided, and add it to the list of clues"""
        definitions = self.word_dict[word.string][1]
        clue = Clue(word.string, len(self.clues), word.orientation, definitions, word.start_row, word.start_col)
        self.clues.append(clue)

    def _generate_new_word(self):
        """Generates one new word in the crossword, if possible"""

        # Shuffle the intersections list and pop the last one
        intersection_list = list(self.intersections)
        random.shuffle(intersection_list)
        root_cell = intersection_list.pop()
        self.intersections.remove(root_cell)
        (start_row, start_col, orientation) = root_cell

        # Remember the original intersection point, as this must remain
        # part of the word if it needs to be shortened due to lack of a match
        original_row = start_row
        original_col = start_col

        # Create a list to hold the characters that will appear in the word, and
        # add the character at the intersection point to it
        candidate = []
        candidate.append(self.grid[original_row][original_col])
        
        # Probe the existing crossword grid forwards, and then backwards, to generate
        # the longest possible word than includes the intersection point
        if orientation == Orientation.VERTICAL:
            row = start_row + 1
            while row < self.rows:
                if self._check_cell_is_legal(row, start_col, Orientation.VERTICAL):
                    candidate.append(self.grid[row][start_col])
                else:
                    break
                row += 1
            row = start_row - 1
            while row >= 0:
                if self._check_cell_is_legal(row, start_col, Orientation.VERTICAL):
                    candidate.insert(0, self.grid[row][start_col])

                    # Move the root row back to match the new legal start to the potential word
                    start_row = row
                else:
                    break
                row -= 1
        elif orientation == Orientation.HORIZONTAL:
            col = start_col + 1
            while col < self.cols:
                if self._check_cell_is_legal(start_row, col, Orientation.HORIZONTAL):
                    candidate.append(self.grid[start_row][col])
                else:
                    break
                col += 1
            col = start_col - 1
            while col >= 0:
                if self._check_cell_is_legal(start_row, col, Orientation.HORIZONTAL):
                    candidate.insert(0, self.grid[start_row][col])

                    # Move the root column back to match the new legal start to the potential word
                    start_col = col
                else:
                    break
                col -= 1

        # Words shorter than three characters cannot connect 2 existing words, so ignore them.
        if len(candidate) < 3:
            return None
        matches = find_matches(candidate, self.dict_by_length, self.word_dict)

        # If there is no match, try removing characters from the candidate and finding new matches
        # If no shorter candidate is possible, return None and forget this intersection point
        while len(matches) == 0:
            shorter_candidate = self._get_shorter_candidate(
                                        candidate,
                                        orientation,
                                        start_row,
                                        start_col,
                                        original_row,
                                        original_col)
            if shorter_candidate is None:
                return None
            matches = find_matches(shorter_candidate, self.dict_by_length, self.word_dict)

        choice = matches[0]
        return Word(orientation, choice, start_row, start_col)

    def _get_shorter_candidate(self, candidate, orientation, start_row, start_col, original_row, original_col):
        if orientation == Orientation.HORIZONTAL:
            # 3 is the minimum word length, and the word must include the original intersection
            while len(candidate) > 3 and start_col + len(candidate) > original_col:
                # While cells can still be removed, remove the last one. If it is empty, 
                # then this new candidate does not abut an existing word, so return it
                removed_cell = candidate.pop()
                if removed_cell == '_':
                    return candidate
            # No shorter candidates are possible, so return None
            return None
        elif orientation == Orientation.VERTICAL:
            # 3 is the minimum word length, and the word must include the original intersection
            while len(candidate) > 3 and start_row + len(candidate) > original_row:
                removed_cell = candidate.pop()
                if removed_cell == '_':
                    return candidate
            # No shorter candidates are possible, so return None
            return None


    def _check_cell_is_legal(self, row, col, orientation):
        """Checks if the cell can be used as part of a new word in the crossword"""

        # If this cell already contains a letter, it is already part of a word
        # running in the orthogonal direction, so it is a legal cell in a potential
        # new word
        if self.grid[row][col] != "_":
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

        for i, _ in enumerate(word.string):
            if word.orientation == Orientation.HORIZONTAL:
                self.grid[word.start_row][word.start_col + i] = word.string[i]
            else:
                self.grid[word.start_row + i][word.start_col] = word.string[i]

        # Calculate the new intersections on this word
        new_start_col = word.start_col
        new_start_row = word.start_row
        new_orientation = word.orientation.opposite()
        
        # A character in the crossword grid belonging to a word can be used
        # as an intersection point for future words as long as it doesn't have
        # occupied neighbouring cells in the direction orthogonal to the word.
        if new_orientation == Orientation.VERTICAL:
            end_col = word.start_col + len(word.string) - 1
            while new_start_col < self.cols:
                cell_above_occupied = self._check_cell_occupied(new_start_row - 1, new_start_col)
                cell_below_occupied = self._check_cell_occupied(new_start_row + 1, new_start_col)
                if not cell_above_occupied and not cell_below_occupied:
                    self.intersections.add((new_start_row, new_start_col, new_orientation))
                new_start_col += 1
                if new_start_col > end_col:
                    break
        elif new_orientation == Orientation.HORIZONTAL:
            end_row = word.start_row + len(word.string) - 1
            while new_start_row < self.rows:
                cell_to_left_occupied = self._check_cell_occupied(new_start_row, new_start_col - 1)
                cell_to_right_occupied = self._check_cell_occupied(new_start_row, new_start_col + 1)
                if not cell_to_left_occupied and not cell_to_right_occupied:
                    self.intersections.add((new_start_row, new_start_col, new_orientation))
                new_start_row += 1
                if new_start_row > end_row:
                    break

    def _check_cell_occupied(self, row, col):
        """Checks if a cell has been filled with a letter or not. Interprets a cell 
           outside the crossword as being empty"""
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return False
        if self.grid[row][col] == '_':
            return False
        return True

    def _prune_intersection_set(self):
        """Removes an intersection from the intersection set if the cell before or after
           it is unusable (already occupied or out of range). This prevents new words being
           added that abut, but do not intersect, existing words in the crossword"""
        temp_set = set()
        for item in self.intersections:
            (row, col, orientation) = item
            cell_before_occupied = False
            cell_after_occupied = False
            if orientation == Orientation.HORIZONTAL:
                if col == 0:
                    cell_before_occupied = False
                if col == self.cols - 1:
                    cell_after_occupied = False
                if col > 0 and self.grid[row][col - 1] != '_':
                    cell_before_occupied = True
                if col < self.cols - 2 and self.grid[row][col + 1] != '_':
                    cell_after_occupied = True
            elif orientation == Orientation.VERTICAL:
                if row == 0:
                    cell_before_occupied = False
                if row == self.rows - 1:
                    cell_after_occupied = False
                if row > 0 and self.grid[row - 1][col] != '_':
                    cell_before_occupied = True
                if row < self.rows - 2 and self.grid[row + 1][col] != '_':
                    cell_after_occupied = True

            if not cell_before_occupied and not cell_after_occupied:
                temp_set.add(item)
        self.intersections = temp_set

    def _print_intersections(self):
        # print("Current intersection set : ")
        string = ""
        for item in self.intersections:
            string += f"{item[0]},{item[1]},{item[2].value} .... "
        # print(string)

    def print(self):
        """Print the crossword to the terminal"""
        light_gray = Colors.get_background_color(220, 220, 220)
        dark_gray = Colors.get_background_color(0, 0, 0)
        text_color = Colors.get_foreground_color(0, 0, 0)
        # print()
        # print("Here's the crossword : ")
        for row in self.grid:
            display_chars = []
            for char in row:
                if char == '_':
                    display_chars.append(f"{dark_gray}  {AnsiCommands.DEFAULT_COLOR}")
                else:
                    display_chars.append(f"{light_gray}{text_color}{get_large_letter(char)}{AnsiCommands.DEFAULT_COLOR}")
            string = ''.join(display_chars)
            print(string)
        

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

def find_matches(word, dict_by_length, word_dict):
    """Searches the word_dict to find matches for the supplied word.
       Returns the list of matches sorted in descending order of
       frequency"""
    known_chars = []
    for i, char in enumerate(word):
        if char != '_':
            known_chars.append((i, char))
    if len(word) not in dict_by_length.keys():
        return []
    potential_matches = dict_by_length[len(word)]
    matches = []
    for potential_match in potential_matches:
        match = True
        for char_tuple in known_chars:
            index, char = char_tuple
            if potential_match[index] != char:
                match = False
        if match:
            matches.append(potential_match)

    # Sort matches based on frequency (descending)
    matches = sorted(matches, key = lambda match: word_dict[match][0], reverse=True)
    # print(matches)
    
    return matches


if __name__ == '__main__':
    main()