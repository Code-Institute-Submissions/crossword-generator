from source.constants import Orientation


def validate(crossword):
    """Performs a suite of tests on a crossword, returning True if all
       pass, False otherwise"""
    crossword.print()
    print()

    print("Checking for 2x2 groups of occupied cells")
    result = check_for_2x2_groups(crossword)
    if result:
        print("  ... All groups valid")
    else:
        return False

    result = check_clue_strings_match_grid(crossword)
    if result:
        print("  ...All clues match grid")
    else:
        return False

    result = check_no_adjacent_clues(crossword)
    if result:
        print("  ...No adjacent clues found")
    else:
        return False

    result = check_all_clues_appear_in_dictionary(crossword)
    if result:
        print("  ...all clues appear in dictionary")
    else:
        return False

    result = check_all_clue_indices_are_unique(crossword)
    if result:
        print(" ...all clue indices are unique")

    return True


def check_for_2x2_groups(crossword):
    """Test ensures that no 2x2 group of contiguous cells are all occupied.
       If such a group is full, it means that there are at least 2 clues
       running parallel to each other 1 square apart, which generates a
       number of extra unwanted 2-letter words"""
    for i in range(crossword.rows - 1):
        for j in range(crossword.cols - 1):
            group = [crossword.grid[i][j],
                     crossword.grid[i][j + 1],
                     crossword.grid[i + 1][j],
                     crossword.grid[i + 1][j + 1]]
            if '_' not in group:
                print(f"Illegal 2x2 group found starting on row {i}, col {j}")
                return False
    return True


def check_clue_strings_match_grid(crossword):
    """Test ensures that all clue strings are represented accurately on the
       crossword grid. This would not be the case if a clue had overwritten
       the letters in another clue"""
    clues = crossword.clues_across + crossword.clues_down
    for clue in clues:
        if clue.orientation == Orientation.HORIZONTAL:
            row = clue.start_row
            for i, char in enumerate(clue.string):
                col = clue.start_col
                grid_char = crossword.grid[row][col + i]
                if char != grid_char:
                    print(f"Characters do not match at row {row}, "
                          f"col {col + i} for {clue.string}")
                    print(f"clue[{i}] == {clue.string[i]} , "
                          f"grid[{row}][{col + i}] == {grid_char}")
                    return False
        elif clue.orientation == Orientation.VERTICAL:
            col = clue.start_col
            for i, char in enumerate(clue.string):
                row = clue.start_row
                grid_char = crossword.grid[row + i][col]
                if char != grid_char:
                    print(f"Characters do not match at row {row + i}, "
                          f"col {col} for {clue.string}")
                    print(f"clue[{i}] == {clue.string[i]} , "
                          f"grid[{row + i}][{col}] == {grid_char}")
                    return False
    return True


def check_no_adjacent_clues(crossword):
    """Test ensures that no clue touches another without intersecting it"""
    clues = crossword.clues_across + crossword.clues_down
    for clue in clues:
        if clue.orientation == Orientation.HORIZONTAL:
            # The cells bookending the clue must be blank
            row = clue.start_row
            length = len(clue.string)
            if clue.start_col > 0:
                if crossword.grid[row][clue.start_col - 1] != '_':
                    print(f"{clue.string} touches another clue at {row},"
                          f"{clue.start_col - 1}")
                    return False
            if clue.start_col + length < crossword.cols - 1:
                if crossword.grid[row][clue.start_col + length] != '_':
                    print(f"{clue.string} touches another clue at {row},"
                          f"{clue.start_col + length}")
                    return False
        elif clue.orientation == Orientation.VERTICAL:
            # The cells bookending the clue must be blank
            col = clue.start_col
            length = len(clue.string)
            if clue.start_row > 0:
                if crossword.grid[clue.start_row - 1][col] != '_':
                    print(f"{clue.string} touches another clue at "
                          f"{clue.start_row - 1},{col}")
                    return False
            if clue.start_row + length < crossword.rows - 1:
                if crossword.grid[clue.start_row + length][col] != '_':
                    print(f"{clue.string} touches another clue at "
                          f"{clue.start_row + length},{col}")
                    return False
    return True


def check_all_clues_appear_in_dictionary(crossword):
    """Test confirms that all clue strings do in fact appear in the
       dictionary"""
    clues = crossword.clues_across + crossword.clues_down
    for clue in clues:
        if clue.string not in crossword.word_dict:
            print(f"The clue '{clue.string}' does not "
                  f"appear in the dictionary")
            return False
    return True


def check_all_clue_indices_are_unique(crossword):
    """Test confirms that no clue index appears twice in either the
       clues_across or clues_down lists"""
    if len(set(crossword.clues_across)) < len(crossword.clues_across):
        print("Duplicate across clue indices:")
        for clue in crossword.clues_across:
            print(clue.index)
        return False
    if len(set(crossword.clues_down)) < len(crossword.clues_down):
        print("Duplicate down clue indices:")
        for clue in crossword.clues_down:
            print(clue.index)
        return False
    return True


if __name__ == '__main__':
    multiple_crossword_validate()
