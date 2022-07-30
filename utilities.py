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