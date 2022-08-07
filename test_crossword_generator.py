from crossword_generator import Crossword
from run import build_dictionary_and_length_map

import pytest

@pytest.fixture
def blank_crossword():
    (word_dict, word_length_map) = build_dictionary_and_length_map()
    blank_crossword = Crossword(7, 7, word_length_map,
                                word_dict, empty=True)
    return blank_crossword

def test_blank_crossword_contains_no_clues(blank_crossword):
    clue_count_across = len(blank_crossword.clues_across)
    clue_count_down = len(blank_crossword.clues_down)
    assert(clue_count_across == 0 and clue_count_down == 0)