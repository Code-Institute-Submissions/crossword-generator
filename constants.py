import enum
import random

class UniChars(str, enum.Enum):
    """ 
    Holds the Unicode characters used in the game 
    """
    MIDDLE_DOT = "\u00B7"
    PLANE_EAST = "\u25B6"
    PLANE_WEST = "\u25C0"
    PLANE_NORTH = "\u25B2"
    PLANE_SOUTH = "\u25BC"
    BOX_HORIZONTAL = "\u2550"
    BOX_VERTICAL = "\u2551"
    BOX_TOP_LEFT = "\u2554"
    BOX_TOP_RIGHT = "\u2557"
    BOX_BOTTOM_RIGHT = "\u255D"
    BOX_BOTTOM_LEFT = "\u255A"
    HORIZONTAL_LINE = "\u2500"
    LEFT_ARROW = "\u27F5"
    STAR = "\u2605"
    SUPERSCRIPT = [
        '\u00B9',
        '\u00B2',
        '\u00B3',
        '\u2074',
        '\u2075',
        '\u2076',
        '\u2077',
        '\u2078',
        '\u2079',
    ]
    EMPTY_SQUARE = "\u2B1C"

    @staticmethod
    def superscript(index):
        """Get a superscript character for this number"""
        if index == 1:
            return '\u00B9'
        elif index == 2:
            return '\u00B2'
        elif index == 3:
            return '\u00B3'
        elif index == 4:
            return '\u2074'
        elif index == 5:
            return '\u2075'
        elif index == 6:
            return '\u2076'
        elif index == 7:
            return '\u2077'
        elif index == 8:
            return '\u2078'
        elif index == 9:
            return '\u2079'
        elif index == 0:
            return '\u2070'
    

class Colors(str, enum.Enum):
    """
    Holds the colors used in the game
    """
    FOREGROUND_BLUE = "\x1b[38;5;12m"
    FOREGROUND_CYAN = "\x1b[38;5;14m"
    FOREGROUND_GREEN = "\x1b[38;5;10m"
    FOREGROUND_YELLOW = "\x1b[38;5;11m"
    FOREGROUND_PURPLE = "\x1b[38;5;13m"
    FOREGROUND_ORANGE = "\x1b[38;5;208m"
    FOREGROUND_RED = "\x1b[38;5;9m"
    FOREGROUND_BLACK = "\x1b[38;5;0m"
    FOREGROUND_WHITE = "\x1b[38;5;15m"
    BACKGROUND_CYAN = "\x1b[48;5;14m"
    BACKGROUND_ORANGE = "\x1b[48;5;208m"
    BACKGROUND_RED = "\x1b[48;5;9m"
    

    @staticmethod
    def random():
        """Choose a random color from the above values"""
        return random.choice(list(Colors))

    @staticmethod
    def random_full():
        """Create a random color"""
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return f"\x1b[38;2;{red};{green};{blue}m"

    @staticmethod
    def get_foreground_color(r, g, b):
        """Return a code to change the foreground color to the values provided"""
        return f"\x1b[38;2;{r};{g};{b}m"

    @staticmethod
    def get_background_color(r, g, b):
        """Return a code to change the background color to the values provided"""
        return f"\x1b[48;2;{r};{g};{b}m"

class AnsiCommands(str, enum.Enum):
    """
    Holds the cursor movement and output deletion commands
    """
    SAVE_CURSOR = f"\x1b7"
    RESTORE_CURSOR = f"\x1b8"
    CARRIAGE_RETURN = f"\r"
    TERMINAL_BELL = f"\a"
    CLEAR_SCREEN = f"\x1b[2J"
    CLEAR_LINE = f"\x1b[2K"
    CLEAR_BUFFER = f"\x1b[3J"
    CURSOR_TO_HOME = f"\x1b[H"
    CURSOR_UP_ONE_LINE = f"\x1b[1A"
    INVERSE_COLOR = f"\x1b[7m"
    BLINK = "\x1b[5m"
    NORMAL = "\x1b[0m"
    FAINT = "\x1b[2m"
    BOLD = "\x1b[1m"
    DEFAULT_COLOR = "\x1b[00m"

class Orientation (enum.Enum):
    """
    Represents the 2 directions a word can be printed in
    """
    HORIZONTAL = "Across"
    VERTICAL = "Down"

    def opposite(self):
        """Returns the orthogonal direction"""
        if self == Orientation.HORIZONTAL:
            return Orientation.VERTICAL
        else:
            return Orientation.HORIZONTAL

class ViewType (enum.Enum):
    """
    Represents the 4 views that the user can cycle through by 
    hitting enter at the command prompt
    """
    CROSSWORD = 0
    CLUES_ACROSS = 1
    CLUES_DOWN = 2
    INSTRUCTIONS = 3

    def next(self):
        """Cycle through the enum values, returning to the first value
           once the last is passed"""
        index = self.value
        index +=1
        if index >= len(list(ViewType)):
            index = 0
        return ViewType(index)


def get_large_letter(char):
    """Returns a large (double width) version of the character supplied"""
    unicode_value = ord(char)
    large_equivalent = unicode_value + 65216

    return chr(large_equivalent)