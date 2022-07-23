from constants import get_large_letter, Colors, UniChars, AnsiCommands

class Word:
    def __init__(self, orientation, string, x, y):
        self.orientation = orientation
        self.string = string
        self.start_x = x
        self.start_y = y

class Crossword:
    """Represents a crossword object"""
    def __init__(self, cols, rows):
        self.grid = [["_" for i in range(cols)] for j in range(rows)]
        self.grid[0][6] = 'a'
        self.grid[0][7] = 's'
        self.print()

    def print(self):
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
    crossword = Crossword(11, 11)


if __name__ == '__main__':
    main()