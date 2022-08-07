from constants import AnsiCommands, Orientation
import sys

def validate(crossword):
    """Performs a suite of tests on a crossword, returning True if all 
       pass, False otherwise"""
    sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    crossword.print()
    print()

    print("Checking for 2x2 groups of occupied cells")
    result = check_for_2x2_groups(crossword)
    if result:
        print("  All groups valid ...")
    else:
        return False

    result = check_clue_strings_match_grid(crossword)
    if result:
        print("  All clues match grid ...")
    else:
        return False

    result = check_no_adjacent_clues(crossword)
    if result:
        print("  No adjacent clues found ...")
    else: return False

def check_for_2x2_groups(crossword):
    """Test ensures that no 2x2 group of contiguous cells are all occupied"""
    for i in range(crossword.rows - 1):
        for j in range(crossword.cols - 1):
            group = []
            group.append(crossword.grid[i][j])
            group.append(crossword.grid[i][j + 1])
            group.append(crossword.grid[i + 1][j])
            group.append(crossword.grid[i + 1][j + 1])
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
                    print(f"Characters do not match at row {row}, col {col + i} for {clue.string}")
                    print(f"clue[{i}] == {clue.string[i]} , grid[{row}][{col + i}] == {grid_char}")
                    return False
        elif clue.orientation == Orientation.VERTICAL:
            col = clue.start_col
            for i, char in enumerate(clue.string):
                row = clue.start_row
                grid_char = crossword.grid[row + i][col]
                if char != grid_char:
                    print(f"Characters do not match at row {row + i}, col {col} for {clue.string}")
                    print(f"clue[{i}] == {clue.string[i]} , grid[{row + i}][{col}] == {grid_char}")
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
                    print(f"{clue.string} touches another clue at {row},{clue.start_col - 1}")
                    return False
            if clue.start_col + length < crossword.cols - 1:
                if crossword.grid[row][clue.start_col + length] != '_':
                    print(f"{clue.string} touches another clue at {row},{clue.start_col + length}")
                    return False
        elif clue.orientation == Orientation.VERTICAL:
            # The cells bookending the clue must be blank
            col = clue.start_col
            length = len(clue.string)
            if clue.start_row > 0:
                if crossword.grid[clue.start_row - 1][col] != '_':
                    print(f"{clue.string} touches another clue at {clue.start_row - 1},{col}")
                    return False
            if clue.start_row + length < crossword.rows - 1:
                if crossword.grid[clue.start_row + length][col] != '_':
                    print(f"{clue.string} touches another clue at {clue.start_row + length},{col}")
                    return False
    return True
