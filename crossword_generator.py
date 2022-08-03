import random
from constants import Orientation, get_large_letter, Colors, AnsiCommands
from utilities import Word, Clue, find_matches

class Crossword:
    """Represents a crossword object"""
    def __init__(self, rows, cols, word_length_map, word_dict):
        self.cols = cols
        self.rows = rows
        self.grid = [["_" for i in range(rows)] for j in range(cols)]
        self.user_guesses = [["_" for i in range(rows)] for j in range(cols)]
        self.word_dict = word_dict
        self.word_length_map = word_length_map
        self.clues_across = []
        self.clues_down = []
        self.selected_clue = None

        # A set is used to prevent duplicate intersections
        self.intersections = set()
        
        # Generate a random crossword layout
        self.generate_words()
        self.reindex_clues()
        self.selected_clue = self.clues_across[0]
        self.print()

    def generate_words(self):
        """This function generates the words for the crossword"""

        # Create the initial blank string for the first word in the crossword, 
        # choosing a string oriented across of random length.
        blank_chars = ['_' for i in range(random.randint(3, self.cols - 1))]
        blank_string = ''.join(blank_chars)
        
        # Find words matching this initial string, and add it to a random row.
        matches = find_matches(blank_string, self.word_length_map, self.word_dict)
        choice = matches[0]
        random_row = random.randint(0, self.rows - 1)
        first_word = Word(Orientation.HORIZONTAL, choice, random_row, 0)
        self.add_word_to_grid(first_word)
        self.add_word_to_clues(first_word)
        
        # Loop that generates all subsequent words. Each time a word is generated,
        # one intersection is removed, and more are added. Not all of these are usable.
        while len(self.intersections) > 0:
            next_word = self._generate_new_word()
            if next_word is not None:
                self.add_word_to_grid(next_word)
                self.add_word_to_clues(next_word)
                self.print()
                self._prune_intersection_set()

    def add_word_to_clues(self, word):
        """Derive a clue from the word provided, and add it to the list of clues"""
        definitions = self.word_dict[word.string][1]
        if word.orientation == Orientation.HORIZONTAL:
            clue = Clue(word.string, len(self.clues_across) + 1, word.orientation, definitions, word.start_row, word.start_col)
            self.clues_across.append(clue)
        else:
            clue = Clue(word.string, len(self.clues_down) + 1, word.orientation, definitions, word.start_row, word.start_col)
            self.clues_down.append(clue)

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
        max_lengths = [6, 7, 8, 9, 10]
        max_length = random.choice(max_lengths)
        candidate = []
        candidate.append(self.grid[original_row][original_col])
        
        # Probe the existing crossword grid forwards, and then backwards, to generate
        # the longest possible word than includes the intersection point
        if orientation == Orientation.VERTICAL:
            row = start_row + 1
            while row < self.rows and len(candidate) < max_length:
                if self._check_cell_is_legal(row, start_col, Orientation.VERTICAL):
                    candidate.append(self.grid[row][start_col])
                else:
                    break
                row += 1
            row = start_row - 1
            while row >= 0 and len(candidate) < max_length:
                if self._check_cell_is_legal(row, start_col, Orientation.VERTICAL):
                    candidate.insert(0, self.grid[row][start_col])

                    # Move the root row back to match the new legal start to the potential word
                    start_row = row
                else:
                    break
                row -= 1
        elif orientation == Orientation.HORIZONTAL:
            col = start_col + 1
            while col < self.cols and len(candidate) < max_length:
                if self._check_cell_is_legal(start_row, col, Orientation.HORIZONTAL):
                    candidate.append(self.grid[start_row][col])
                else:
                    break
                col += 1
            col = start_col - 1
            while col >= 0 and len(candidate) < max_length:
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
        matches = find_matches(candidate, self.word_length_map, self.word_dict)

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
            matches = find_matches(shorter_candidate, self.word_length_map, self.word_dict)

        choice = random.choice(matches)
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

    def add_word_to_grid(self, word):
        """Adds a word to the crossword grid in the correct orientation"""

        for i, _ in enumerate(word.string):
            if word.orientation == Orientation.HORIZONTAL:
                self.grid[word.start_row][word.start_col + i] = word.string[i]
                self.user_guesses[word.start_row][word.start_col + i] = '*'
            else:
                self.grid[word.start_row + i][word.start_col] = word.string[i]
                self.user_guesses[word.start_row + i][word.start_col] = '*'

        # Remove the word from the dict_by_length dictionary so that it cannot
        # appear twice. This prevents it appearing again in any crossword created
        # in this instance of the program.
        key = len(word.string)
        self.word_length_map[key].remove(word.string)

        # Calculate the new intersections on this word
        new_start_col = word.start_col
        new_start_row = word.start_row
        new_orientation = word.orientation.opposite()
        
        # A character in the crossword grid belonging to a word can be used
        # as an intersection point for future words as long as it doesn't have
        # occupied neighbouring cells in the direction orthogonal to the word,
        # i.e. if the intersection was already being used by 2 words.
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

    def has_clue(self, index, orientation):
        """Returns true if a clue with the supplied index and orientation
           exists in the crossword"""
        clue_exists = False
        if orientation == Orientation.HORIZONTAL:
            for clue in self.clues_across:
                if clue.index == index:
                    clue_exists = True
        elif orientation == Orientation.VERTICAL:
            for clue in self.clues_down:
                if clue.index == index:
                    clue_exists = True
        return clue_exists

    def get_clue(self, index, orientation):
        """Gets a clue from one of the lists of clues based on index and
           orientation"""
        requested_clue = None
        if orientation == Orientation.HORIZONTAL:
            for clue in self.clues_across:
                if clue.index == index:
                    requested_clue = clue
        elif orientation == Orientation.VERTICAL:
            for clue in self.clues_down:
                if clue.index == index:
                    requested_clue = clue
        return requested_clue
        
    def reindex_clues(self):
        """Reindexes the clues so that they are ordered from left to right, and
           top to bottom. Ensures that clues across and down that share the same
           start_cell in the crossword grid use the same index, as only one
           index can be printed per cell in the terminal"""
        
        # Create a dictionary, to hold the clues keyed by a tuple containing the
        # start_col and start_row
        clues_dict = {}

        clues_across_reindexed = []
        clues_down_reindexed = []
        clues_list = self.clues_across + self.clues_down

        # Iterate throught the combined list of clues, and populate the dictionary
        for clue in clues_list:
            start_cell = (clue.start_col, clue.start_row)
            if start_cell in clues_dict:
                clues_dict[start_cell].append(clue)
            else:
                clues_dict[start_cell] = []
                clues_dict[start_cell].append(clue)

        # Keep a counter for the next indices of across and down clues respectively
        across_counter = 1
        down_counter = 1

        # Keep track of already the down indices already used, so that they are not
        # duplicated.
        unusable_down_indices = []

        # Iterate through the dictionary
        for start_cell, clues_list in sorted(clues_dict.items()):
            if len(clues_list) > 1:
                # There is an across clue and a down clue starting in the same cell
                for clue in clues_list:
                    if clue.orientation == Orientation.HORIZONTAL:
                        # Give the across clue its next index
                        clue.index = across_counter
                        clues_across_reindexed.append(clue)
                    elif clue.orientation == Orientation.VERTICAL:
                        # Give the down clue the SAME index, and add
                        # it to the list of used down indices
                        clue.index = across_counter
                        clues_down_reindexed.append(clue)
                        unusable_down_indices.append(across_counter)
                # Increment the across_counter
                across_counter += 1
            else:
                # This clue has a unique starting cell
                if clues_list[0].orientation == Orientation.HORIZONTAL:
                    clues_list[0].index = across_counter
                    clues_across_reindexed.append(clues_list[0])
                    across_counter += 1
                elif clues_list[0].orientation == Orientation.VERTICAL:
                    # Don't reuse an index. Increment until a fresh one
                    # is found
                    while down_counter in unusable_down_indices:
                        down_counter += 1
                    clues_list[0].index = down_counter
                    unusable_down_indices.append(down_counter)
                    down_counter += 1
                    clues_down_reindexed.append(clues_list[0])

        # The clues_across_reindexed list is already in order
        self.clues_across = clues_across_reindexed
        # The clues_down_reindexed list may not be, as it may have shared
        # an index with an across clue
        self.clues_down = sorted(clues_down_reindexed, key=lambda clue: clue.index)

    def print(self):
        """Print the crossword to the terminal"""
        light_gray = Colors.get_background_color(220, 220, 220)
        dark_gray = Colors.get_background_color(0, 0, 0)
        text_color = Colors.get_foreground_color(0, 0, 0)
        
        for row in self.grid:
            display_chars = []
            for char in row:
                if char == '_':
                    display_chars.append(f"{dark_gray}  {AnsiCommands.DEFAULT_COLOR}")
                else:
                    display_chars.append(f"{light_gray}{text_color}{get_large_letter(char)}{AnsiCommands.DEFAULT_COLOR}")
            string = ''.join(display_chars)
            print(string)
