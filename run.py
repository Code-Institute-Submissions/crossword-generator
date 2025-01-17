"""
This file is the main entry point for the program. It loads the word
dictionary from file and creates a word length map from this data.
It then creates a new crossword puzzle, validates it, and then begins
the user input loop to let the user attempt the puzzle
"""
import sys
import json
from collections import defaultdict

from source.crossword_generator import Crossword
from source.utilities import (draw_string, get_move_cursor_string,
                              get_alternating_square_color)
from source.constants import (AnsiCommands, Colors, UniChars, Orientation,
                              ViewType, get_large_letter)
from source.crossword_validator import validate

TERMINAL_WIDTH = 80
TERMINAL_HEIGHT = 24
START_ROW = 2
START_COL = 2
LIGHT_GRAY = Colors.get_background_color(220, 220, 220)
MEDIUM_GRAY = Colors.get_background_color(180, 180, 180)
DARK_GRAY = Colors.get_background_color(40, 40, 40)
TEXT_COLOR = Colors.get_foreground_color(0, 0, 0)


def main():
    """Main entry point for the program"""
    (word_dict, word_length_map) = build_dictionary_and_length_map()
    crossword = Crossword(13, 13, word_length_map, word_dict)
    validate(crossword)

    begin_puzzle(crossword)


def build_dictionary_and_length_map():
    """Import the word dictionary from file, and use it to build
       a map of words keyed by their lengths"""
    word_length_map = defaultdict(lambda: [])
    with open('data/crossword_dictionary.json', 'r', encoding='utf-8') as file:
        word_dict = json.load(file)

        # Build a python dictionary with word lengths as keys, and lists of
        # words of that length as values. The dictionary is used to search for
        # matching partial words
        for word in word_dict.keys():
            word = word.replace('\n', '')
            length = len(word)
            word_length_map[length].append(word)
    return word_dict, word_length_map


def begin_puzzle(crossword):
    """Allows the user to begin solving the puzzle"""
    current_view = ViewType.INSTRUCTIONS
    display_instructions(current_view)

    while True:
        input_y_pos = TERMINAL_HEIGHT - 2
        sys.stdout.write(get_move_cursor_string(0, input_y_pos + 1))
        sys.stdout.write(AnsiCommands.CLEAR_LINE)
        sys.stdout.write(get_move_cursor_string(0, input_y_pos))
        sys.stdout.write(AnsiCommands.CLEAR_LINE)
        sys.stdout.flush()
        msg = ("Enter answer, select clue (e.g. '2 across'), "
               "or hit enter to change view :\n")
        if current_view == ViewType.CLUES_DOWN \
                or current_view == ViewType.CLUES_ACROSS:
            msg = "Hit enter to change view: \n"
        elif current_view == ViewType.INSTRUCTIONS:
            msg = "Hit enter to move to crossword view\n"
        command = input(f"{AnsiCommands.BOLD}{Colors.FOREGROUND_WHITE}{msg}")
        if command != '':
            # The user may be entering the solution to a clue, or
            # requesting a clue to be displayed
            result = parse_command(command, crossword, current_view)
            user_message = f"{AnsiCommands.CLEAR_LINE}{result}"
            draw_string(user_message,
                        0,
                        TERMINAL_HEIGHT,
                        [Colors.FOREGROUND_RED])
            current_view = ViewType.CROSSWORD
        else:
            # The user is toggling through the views
            current_view = current_view.next()
            if current_view == ViewType.CROSSWORD:
                display_crossword(crossword, current_view)
                highlight_single_clue(crossword)
            elif current_view == ViewType.CLUES_ACROSS:
                display_clues(crossword, Orientation.HORIZONTAL, current_view)
            elif current_view == ViewType.CLUES_DOWN:
                display_clues(crossword, Orientation.VERTICAL, current_view)
            elif current_view == ViewType.INSTRUCTIONS:
                display_instructions(current_view)


def display_instructions(current_view):
    """Prints the instructions to the display"""
    style = (
        f"{AnsiCommands.CLEAR_BUFFER}{AnsiCommands.CLEAR_SCREEN}"
        f"{AnsiCommands.BOLD}{Colors.FOREGROUND_WHITE}"
    )
    title = "INSTRUCTIONS".center(80)
    draw_string(style + title, 0, 2, [])
    style = f"{AnsiCommands.NORMAL}"
    para1 = (
        " There are two crossword puzzles next to each other on the main page."
        "\n"
        " The puzzle on the left just shows the clue numbers in the starting\n"
        " square of each clue. The puzzle on the right show the answers that\n"
        " you've already entered.\n\n"
        " Pressing enter repeatedly allow you to tab through the 4 views\n\n"
        "   1) The main game view, showing the 2 crosswords and the current"
        " clue\n"
        "   2) All of the Across clues\n"
        "   3) All of the Down clues\n"
        "   4) This instructions page again!\n\n"
        " To enter your answer for the current clue, simply type it into the"
        " terminal.\n"
        " To switch to another clue, enter its description, e.g. '2 across' or"
        " '7 down'.\n"
        " To ask for an alternative clue, enter '?'")
    draw_string(style + para1, 0, 4, [])
    print_view_type_bar(current_view)


def display_crossword(crossword, current_view):
    """Print the crossword to the screen"""
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
    sys.stdout.flush()
    half_screen_width = int(TERMINAL_WIDTH / 2)
    # Each cell of the puzzle requires 2 squares
    half_puzzle_width = int(crossword.cols)

    # The top left corner of the first puzzle
    origin_left = int(TERMINAL_WIDTH / 4) - half_puzzle_width

    # The top left corner of the second puzzle
    origin_right = origin_left + half_screen_width

    # Print a view of the crossword with blank squares where a letter occurs
    # in the grid. This view, on the left, will show the clue indices and
    # highlight the currently selected clue
    for i, row in enumerate(crossword.grid):
        sys.stdout.write(get_move_cursor_string(origin_left, START_ROW + i))
        sys.stdout.flush()
        for j, col in enumerate(row):
            if crossword.grid[i][j] == '_':
                sys.stdout.write(f"{DARK_GRAY}  {AnsiCommands.DEFAULT_COLOR}")
            else:
                char = crossword.grid[i][j].upper()
                color = get_alternating_square_color(i, j)
                output = f"{color}{TEXT_COLOR}  {AnsiCommands.DEFAULT_COLOR}"
                sys.stdout.write(output)
    sys.stdout.flush()

    # Print a second view of the crossword on the right. This view displays
    # the solutions entered by the user
    for i, row in enumerate(crossword.user_guesses):
        sys.stdout.write(get_move_cursor_string(origin_right, START_ROW + i))
        sys.stdout.flush()
        for j, col in enumerate(row):
            if crossword.user_guesses[i][j] == '_':
                sys.stdout.write(f"{DARK_GRAY}  {AnsiCommands.DEFAULT_COLOR}")
            else:
                user_guess = crossword.user_guesses[i][j]
                char = None
                if user_guess == '*':
                    char = '  '
                else:
                    char = get_large_letter(user_guess)
                color = get_alternating_square_color(i, j)
                output = (f"{color}{TEXT_COLOR}{char}"
                          f"{AnsiCommands.DEFAULT_COLOR}")
                sys.stdout.write(output)
    sys.stdout.flush()

    # Print the clue indices on the starting square of each clue.
    sys.stdout.write(TEXT_COLOR)
    for clue in crossword.clues_across:
        first_digit = ''
        second_digit = ''
        if clue.index <= 9:
            first_digit = UniChars.superscript(clue.index)
        else:
            first_digit = f"{UniChars.superscript(int(clue.index / 10))}"
            second_digit = f"{UniChars.superscript(clue.index % 10)}"

        row = START_ROW + clue.start_row
        col = origin_left + clue.start_col * 2
        sys.stdout.write(get_move_cursor_string(col, row))
        color = get_alternating_square_color(clue.start_row, clue.start_col)
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

        row = START_ROW + clue.start_row
        col = origin_left + clue.start_col * 2
        sys.stdout.write(get_move_cursor_string((col), row))
        color = get_alternating_square_color(clue.start_row, clue.start_col)
        sys.stdout.write(f"{color}")
        sys.stdout.write(f"{first_digit}{second_digit}")
    sys.stdout.write(AnsiCommands.DEFAULT_COLOR)
    sys.stdout.flush()

    print_view_type_bar(current_view)


def display_clues(crossword, orientation, current_view):
    """Print the clues to the screen"""
    start_col = 1
    start_row = 2
    sys.stdout.write(AnsiCommands.CLEAR_SCREEN)
    sys.stdout.write(AnsiCommands.CLEAR_BUFFER)
    sys.stdout.write(get_move_cursor_string(start_col, start_row))
    sys.stdout.flush()

    if orientation == Orientation.HORIZONTAL:
        sys.stdout.write(f"{AnsiCommands.BOLD}{Colors.FOREGROUND_WHITE}")
        for char in 'across':
            sys.stdout.write(get_large_letter(char))
        print()
        sys.stdout.write(f"{AnsiCommands.NORMAL}{AnsiCommands.DEFAULT_COLOR}")
        for clue in crossword.clues_across:
            print(f"({clue.index} {clue.orientation.value})"
                  f" ({len(clue.string)}) {clue.definitions[0]}")
    else:
        sys.stdout.write(f"{AnsiCommands.BOLD}{Colors.FOREGROUND_WHITE}")
        for char in 'down':
            sys.stdout.write(get_large_letter(char))
        print()
        sys.stdout.write(f"{AnsiCommands.NORMAL}{AnsiCommands.DEFAULT_COLOR}")
        for clue in crossword.clues_down:
            print(f"({clue.index} {clue.orientation.value})"
                  f" ({len(clue.string)}) {clue.definitions[0]}")

    print_view_type_bar(current_view)


def highlight_single_clue(crossword):
    """Highlight the position of one clue on the crossword puzzle, and print
       that clue below the crossword"""
    clue = crossword.selected_clue

    half_screen_width = int(TERMINAL_WIDTH / 2)

    # Each cell of the puzzle requires 2 squares
    half_puzzle_width = int(crossword.cols)

    # The top left corner of the first puzzle
    origin_left = int(TERMINAL_WIDTH / 4) - half_puzzle_width

    # The top left corner of the second puzzle
    origin_right = origin_left + half_screen_width

    x_coord = origin_left + clue.start_col * 2
    y_coord = START_ROW + clue.start_row
    back = Colors.BACKGROUND_ORANGE
    fore = Colors.FOREGROUND_WHITE
    draw_string("  ", x_coord, y_coord, [fore, back])
    first_digit = ''
    second_digit = ''
    if clue.index <= 9:
        first_digit = UniChars.superscript(clue.index)
    else:
        first_digit = UniChars.superscript(int(clue.index / 10))
        second_digit = UniChars.superscript(clue.index % 10)

    # Draw the clue index in superscript in the starting cell of the clue
    draw_string(
        f"{first_digit}{second_digit}",
        x_coord,
        y_coord,
        [back, fore])

    # Color the succeeding squares of the clue in ORANGE
    if clue.orientation == Orientation.HORIZONTAL:
        for offset in range(1, len(clue.string)):
            back = Colors.BACKGROUND_ORANGE
            draw_string("  ", x_coord + offset * 2, y_coord, [fore, back])
    elif clue.orientation == Orientation.VERTICAL:
        for offset in range(1, len(clue.string)):
            back = Colors.BACKGROUND_ORANGE
            draw_string("  ", x_coord, y_coord + offset, [back, fore])

    # Highlight the corresponding squares of the solution view
    x_coord = origin_right + clue.start_col * 2
    if clue.orientation == Orientation.HORIZONTAL:
        for offset, _ in enumerate(clue.string):
            back = Colors.BACKGROUND_ORANGE
            fore = Colors.FOREGROUND_WHITE
            col = clue.start_col + offset
            guess = crossword.user_guesses[clue.start_row][col]
            char = "  " if guess == "*" else get_large_letter(guess)
            draw_string(char, x_coord + offset * 2, y_coord, [fore, back])
    elif clue.orientation == Orientation.VERTICAL:
        for offset, _ in enumerate(clue.string):
            back = Colors.BACKGROUND_ORANGE
            fore = Colors.FOREGROUND_WHITE
            row = clue.start_row + offset
            guess = crossword.user_guesses[row][clue.start_col]
            char = "  " if guess == "*" else get_large_letter(guess)
            draw_string(char, x_coord, y_coord + offset, [back, fore])

    # Print the clue text just below the views of the crossword puzzle
    sys.stdout.write(AnsiCommands.DEFAULT_COLOR)
    sys.stdout.write(AnsiCommands.BOLD)
    text_display_y = START_ROW + crossword.rows + 1
    sys.stdout.write(get_move_cursor_string(0, text_display_y))
    length = len(clue.string)
    orientation = clue.orientation.value
    string = (
        f"{Colors.FOREGROUND_ORANGE}{clue.index} {orientation} "
        f"{Colors.FOREGROUND_YELLOW}({length}) "
        f"{Colors.FOREGROUND_ORANGE}"
        f"{clue.definitions[clue.current_definition]}")
    sys.stdout.write(string)
    sys.stdout.write(AnsiCommands.DEFAULT_COLOR)
    sys.stdout.flush()


def parse_command(command, crossword, current_view):
    """Parse a command entered by the user. This can be either a request
       to display a different clue, or a solution to the clue currently
       displayed"""

    # If the command is just a single question mark, iterate through this
    # clue's definitions, returning to the first one if the end of the list is
    # reached.
    if command == '?':
        clue = crossword.selected_clue
        if len(clue.definitions) == 1:
            return "There's only one clue for that word!"
        index = clue.current_definition
        index += 1
        if index >= len(clue.definitions):
            index = 0
        clue.current_definition = index
        display_crossword(crossword, current_view)
        highlight_single_clue(crossword)
        return "Showing alternative clue"

    elements = command.split(' ')
    if elements[0].isnumeric():
        if len(elements) == 1:
            return f"Enter {elements[0]} followed by 'down' or 'across'"
        index = int(elements[0])
        # Check if this is a valid reference to a clue, and if so, highlight
        # that clue
        if elements[1].lower() == 'd' or elements[1].lower() == 'down':
            if crossword.has_clue(index, Orientation.VERTICAL):
                new_clue = crossword.get_clue(index, Orientation.VERTICAL)
                display_crossword(crossword, current_view)
                crossword.selected_clue = new_clue
                highlight_single_clue(crossword)
                return f"Now showing {index} Down"
            else:
                return f'No clue matches {elements[0]} {elements[1]}!'
        elif elements[1].lower() == 'a' or elements[1].lower() == 'across':
            if crossword.has_clue(index, Orientation.HORIZONTAL):
                new_clue = crossword.get_clue(index, Orientation.HORIZONTAL)
                display_crossword(crossword, current_view)
                crossword.selected_clue = new_clue
                highlight_single_clue(crossword)
                return f"Now displaying {index} Across"
            else:
                return f'No clue matches {elements[0]} {elements[1]}!'
        else:
            return 'No such clue!'
    else:
        # Check if command is a valid solution to the current clue
        # First ensure the command consists entirely of letters
        if not command.isalpha():
            return 'Solutions can only contain letters!'

        # Next check if the command is the correct length
        if len(command) != len(crossword.selected_clue.string):
            return (f"Wrong length! Length of solution should be "
                    f"{len(crossword.selected_clue.string)}")

        # Guess is correct length and consists only of letters. Enter it in the
        # crossword.user_guesses array and draw the crossword views again to
        # display the updated solution to the user
        word = elements[0].lower()
        clue = crossword.selected_clue
        for i, char in enumerate(word):
            if clue.orientation == Orientation.HORIZONTAL:
                col = clue.start_col + i
                crossword.user_guesses[clue.start_row][col] = char
            else:
                row = clue.start_row + i
                crossword.user_guesses[row][clue.start_col] = char
        display_crossword(crossword, current_view)

        if check_crossword_complete(crossword):
            return "You've cracked it! The crossword is completed!"
        return f"Your answer '{word}' has been entered in the puzzle."


def check_crossword_complete(crossword):
    """Checks each clue's characters against the user_guesses grid, and returns
       False as soon as it finds one that doesn't match. Returns True if all
       are correct"""
    all_clues = crossword.clues_across + crossword.clues_down
    for clue in all_clues:
        for offset, char in enumerate(clue.string):
            if clue.orientation == Orientation.HORIZONTAL:
                col = clue.start_col + offset
                guess_char = crossword.user_guesses[clue.start_row][col]
                if char != guess_char:
                    return False
            else:
                row = clue.start_row + offset
                guess_char = crossword.user_guesses[row][clue.start_col]
                if char != guess_char:
                    return False
    return True


def print_view_type_bar(current_view, in_flow=False):
    """Display the ViewType selection bar at the bottom of the display"""
    y_pos = TERMINAL_HEIGHT - 4
    tab_width = int(TERMINAL_WIDTH / 4) - 4
    output = ""
    for view_type in list(ViewType):
        string = view_type.name.center(tab_width)
        if current_view is view_type:
            output += Colors.get_background_color(150, 50, 50)
            output += Colors.FOREGROUND_WHITE
            output += AnsiCommands.BOLD
            output += string
            output += AnsiCommands.NORMAL
        else:
            output += Colors.get_background_color(200, 200, 200)
            output += Colors.FOREGROUND_BLACK
            output += string
        output += Colors.get_background_color(150, 150, 150)
        output += Colors.FOREGROUND_BLACK
        output += " >> "
        output += AnsiCommands.DEFAULT_COLOR
    if in_flow:
        print(output)
    else:
        draw_string(output, 0, y_pos, [])


if __name__ == '__main__':
    main()
