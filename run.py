import sys
import json
from crossword_generator import Crossword
from utilities import get_move_cursor_string, get_alternating_sqaure_color
from constants import AnsiCommands, Colors, get_large_letter, UniChars

TERMINAL_WIDTH = 80
TERMINAL_HEIGHT = 24
LIGHT_GRAY = Colors.get_background_color(220, 220, 220)
MEDIUM_GRAY = Colors.get_background_color(180, 180, 180)
DARK_GRAY = Colors.get_background_color(40, 40, 40)
TEXT_COLOR = Colors.get_foreground_color(0, 0, 0)

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
    crossword = Crossword(17, 17, dict_by_length, word_dict)

    begin_puzzle(crossword)

def begin_puzzle(crossword):
    """Allows the user to begin solving the puzzle"""
    display_crossword(crossword)
    displayed = 'crossword'
    # display_instructions()

    while True:
        print()
        sys.stdout.write(get_move_cursor_string(0, 3 + crossword.rows))
        input('Enter a command :')
        if displayed == 'crossword':
            displayed = 'clues'
            display_clues(crossword)
        elif displayed == 'clues':
            displayed = 'crossword'
            display_crossword(crossword)

def display_crossword(crossword):
    """Print the crossword to the screen"""
    start_col = 2
    start_row = 2
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
    sys.stdout.flush()
    for i, row in enumerate(crossword.grid):
        sys.stdout.write(get_move_cursor_string(start_col, start_row + i))
        sys.stdout.flush()
        for j, col in enumerate(row):
            if crossword.grid[i][j] == '_':
                sys.stdout.write(f"{DARK_GRAY}  {AnsiCommands.DEFAULT_COLOR}")
            else:
                char = crossword.grid[i][j].upper()
                color = get_alternating_sqaure_color(i, j)
                output = f"{color}{TEXT_COLOR}  {AnsiCommands.DEFAULT_COLOR}"
                sys.stdout.write(output)
    sys.stdout.flush()

    start_col = 6 + crossword.cols * 2
    for i, row in enumerate(crossword.grid):
        sys.stdout.write(get_move_cursor_string(start_col, start_row + i))
        sys.stdout.flush()
        for j, col in enumerate(row):
            if crossword.grid[i][j] == '_':
                sys.stdout.write(f"{DARK_GRAY}  {AnsiCommands.DEFAULT_COLOR}")
            else:
                char = crossword.grid[i][j].upper()
                color = get_alternating_sqaure_color(i, j)
                output = f"{color}{TEXT_COLOR}  {AnsiCommands.DEFAULT_COLOR}"
                sys.stdout.write(output)
    sys.stdout.flush()

    start_col = 2
    sys.stdout.write(TEXT_COLOR)
    for clue in crossword.clues_across:
        first_digit = ''
        second_digit = ''
        if clue.index <= 9:
            first_digit = UniChars.superscript(clue.index)
        else:
            first_digit = f"{UniChars.superscript(int(clue.index / 10))}"
            second_digit = f"{UniChars.superscript(clue.index % 10)}"

        row = start_row + clue.start_row
        col = start_col + clue.start_col
        sys.stdout.write(get_move_cursor_string((col - 1) * 2, row))
        color = get_alternating_sqaure_color(row, col)
        sys.stdout.write(f"{color}")
        sys.stdout.write(f"{first_digit}{second_digit}")

    for clue in crossword.clues_down:
        first_digit = ''
        second_digit = ''
        if clue.index <= 9:
            first_digit = UniChars.superscript(clue.index)
        else:
            first_digit = f"{UniChars.superscript(int(clue.index / 10))}"
            second_digit = f"{UniChars.superscript(clue.index % 10)}"

        row = start_row + clue.start_row
        col = start_col + clue.start_col
        sys.stdout.write(get_move_cursor_string((col - 1) * 2, row))
        color = get_alternating_sqaure_color(row, col)
        sys.stdout.write(f"{color}")
        sys.stdout.write(f"{first_digit}{second_digit}")
    sys.stdout.write(AnsiCommands.DEFAULT_COLOR)
    sys.stdout.flush()

def display_clues(crossword):
    """Print the clues to the screen"""
    start_col = 1
    start_row = 2
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
    sys.stdout.write(get_move_cursor_string(start_col, start_row))
    sys.stdout.flush()
    for clue in crossword.clues_across:
        print(f"({clue.index} {clue.orientation.value}) {clue.definitions[0]}")
    for clue in crossword.clues_down:
        print(f"({clue.index} {clue.orientation.value}) {clue.definitions[0]}")

if __name__ == '__main__':
    main()