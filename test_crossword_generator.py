from crossword_generator import Crossword
from run import build_dictionary_and_length_map

import pytest
from constants import Orientation

@pytest.fixture
def blank_puzzle():
    (word_dict, word_length_map) = build_dictionary_and_length_map()
    return Crossword(7, 7, word_length_map,
                                word_dict, empty=True)

def test_blank_crossword_contains_no_clues(blank_puzzle):
    """Tests that the crossword fixture used here has no clues"""
    clue_count_across = len(blank_puzzle.clues_across)
    clue_count_down = len(blank_puzzle.clues_down)
    assert(clue_count_across == 0 and clue_count_down == 0)

def test_trim_candidate_returns_none_for_candidate_length_three(blank_puzzle):
    """Tests that the function doesn't reduce a candidates length below 3"""
    candidate = ["a", "b", "c"]
    result = blank_puzzle.trim_candidate(candidate, Orientation.VERTICAL, 0, 0, 0, 0)
    assert(result is None)

def test_trim_candidate_returns_shorter_candidate(blank_puzzle):
    """Tests that the function returns a shorter candidate given no constraints"""
    candidate = ["_", "_", "_", "_"]
    original_length = len(candidate)
    result = blank_puzzle.trim_candidate(candidate, Orientation.VERTICAL, 0, 0, 0, 0)
    assert(len(result) < original_length)

def test_trim_candidate_returns_candidate_not_touching_other_word(blank_puzzle):
    """Tests that the candidate will not touch another word without intersecting
       it. Note that a character that is not blank in a candidate must be a part
       of an already existing word in the crossword puzzle"""
    candidate = ["_", "_", "_", "_", "_", "n"]
    original_length = len(candidate)
    result = blank_puzzle.trim_candidate(candidate, Orientation.VERTICAL, 0, 0, 0, 0)
    assert(len(result) == original_length - 2)

def test_trim_candidate_returns_none_for_original_cell_as_last_char(blank_puzzle):
    """Tests that the function does not remove the original cell. The original cell
       is the cell the candidate was generated from - the point of intersection
       with its parent word"""
    candidate = ["_", "_", "_", "_", "x"]
    result_horizontal = blank_puzzle.trim_candidate(candidate, Orientation.HORIZONTAL,
                                                    0, 0, 0, 4)
    assert(result_horizontal is None)

def test_trim_candidate_returns_none_if_original_cell_not_included(blank_puzzle):
    """Tests that the function returns None if a candidate cannot be shortened
       without removing the original intersection cell"""
    candidate = ["_", "_", "_", "_", "_"]
    orientation = Orientation.HORIZONTAL
    original_col = 4
    result_horizontal = blank_puzzle.trim_candidate(candidate, orientation, 0, 0,
                                                    0, original_col)
    assert(result_horizontal is None)

def test_check_for_adjacency_removes_first_character(blank_puzzle):
    """Tests that function removes the first letter of a candidate if it
       touches another word in the puzzle without intersecting it"""
    blank_puzzle.grid[0][0] = "x"
    candidate1 = ["_", "_", "_", "_", "_"]
    candidate2 = candidate1[:]
    length = len(candidate1)
    (result_horizontal, x, y) = blank_puzzle.check_for_adjacency(candidate1,
                                Orientation.HORIZONTAL, 0, 1)
    (result_vertical, x, y) = blank_puzzle.check_for_adjacency(candidate2,
                                Orientation.VERTICAL, 1, 0)
    len_horizontal = len(result_horizontal)
    len_vertical = len(result_vertical)
    assert(len_horizontal == length - 1 and len_vertical == length - 1)