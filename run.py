from constants import get_large_letter

class Crossword:
    """Represents a crossword object"""
    def __init__(self, cols, rows):
        self.grid = [["_" for i in range(cols)] for j in range(rows)]
        self.grid[0][6] = 'a'
        self.grid[0][7] = 's'
        self.print()

    def print(self):
        for row in self.grid:
            display_chars = []
            for char in row:
                if char == '_':
                    display_chars.append('*/')
                else:
                    display_chars.append(get_large_letter(char))
            str = ''.join(display_chars)
            print(str)
        

def main():
    """Main entry point for the program"""
    crossword = Crossword(11, 11)


if __name__ == '__main__':
    main()