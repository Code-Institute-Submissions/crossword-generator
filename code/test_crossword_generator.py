import pytest
from code.crossword_generator import Crossword

@pytest.fixture
def blank_crossword():
    blank_crossword = Crossword(7, 7, word_length_map, 
                                word_dict, empty=True)