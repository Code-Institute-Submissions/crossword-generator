class Crossword:
    """Represents a crossword object"""
    def __init__(self, cols, rows):
        self.grid = [["_" for i in range(cols)] for j in range(rows)]
        self.print()

    def print(self):
        for row in self.grid:
            str = ''.join(row)
            print(str)
        print('\uff2d')
        print('mm')

def main():
    """Main entry point for the program"""
    crossword = Crossword(11, 11)


if __name__ == '__main__':
    main()