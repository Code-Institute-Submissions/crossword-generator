from source.crossword_generator import Crossword
from run import build_dictionary_and_length_map

import pytest
from source.constants import LetterUse, Orientation
from source.utilities import Clue


@pytest.fixture
def blank_puzzle():
    """A crossword containing only empty cells"""
    (word_dict, word_length_map) = build_dictionary_and_length_map()
    return Crossword(7, 7, word_length_map,
                     word_dict, empty=True)


@pytest.fixture
def puzzle_w_clues(blank_puzzle):
    """A empty crossword with six dummy clues, 2 of which share the same
       start cell"""
    clues_across = [Clue("x", 0, Orientation.HORIZONTAL, [], 0, 0),
                    Clue("x", 1, Orientation.HORIZONTAL, [], 3, 0),
                    Clue("x", 2, Orientation.HORIZONTAL, [], 5, 0)]
    clues_down = [Clue("x", 0, Orientation.VERTICAL, [], 0, 4),
                  Clue("x", 1, Orientation.VERTICAL, [], 3, 4),
                  Clue("x", 2, Orientation.VERTICAL, [], 0, 0), ]
    blank_puzzle.clues_across = clues_across
    blank_puzzle.clues_down = clues_down
    return blank_puzzle


def test_blank_crossword_contains_no_clues(blank_puzzle):
    """Tests that the crossword fixture used here has no clues"""
    clue_count_across = len(blank_puzzle.clues_across)
    clue_count_down = len(blank_puzzle.clues_down)
    assert (clue_count_across == 0 and clue_count_down == 0)


def test_trim_candidate_returns_none_for_candidate_length_three(blank_puzzle):
    """Tests that the function doesn't reduce a candidates length below 3"""
    candidate = ["a", "b", "c"]
    result = blank_puzzle.trim_candidate(candidate,
                                         Orientation.VERTICAL, 0, 0, 0, 0)
    assert (result is None)


def test_trim_candidate_returns_shorter_candidate(blank_puzzle):
    """Tests that the function returns a shorter candidate given no constraints"""
    candidate = ["_", "_", "_", "_"]
    original_length = len(candidate)
    result = blank_puzzle.trim_candidate(candidate,
                                         Orientation.VERTICAL, 0, 0, 0, 0)
    assert (len(result) < original_length)


def test_trim_candidate_returns_candidate_not_touching_other_word(blank_puzzle):
    """Tests that the candidate will not touch another word without intersecting
       it. Note that a character that is not blank in a candidate must be a part
       of an already existing word in the crossword puzzle"""
    candidate = ["_", "_", "_", "_", "_", "n"]
    original_length = len(candidate)
    result = blank_puzzle.trim_candidate(candidate,
                                         Orientation.VERTICAL, 0, 0, 0, 0)
    assert (len(result) == original_length - 2)


def test_trim_candidate_returns_none_for_original_cell_as_last_char(blank_puzzle):
    """Tests that the function does not remove the original cell. The original cell
       is the cell the candidate was generated from - the point of intersection
       with its parent word"""
    candidate = ["_", "_", "_", "_", "x"]
    result_horizontal = blank_puzzle.trim_candidate(candidate,
                                                    Orientation.HORIZONTAL,
                                                    0, 0, 0, 4)
    assert (result_horizontal is None)


def test_trim_candidate_returns_none_if_original_cell_not_included(blank_puzzle):
    """Tests that the function returns None if a candidate cannot be shortened
       without removing the original intersection cell"""
    candidate = ["_", "_", "_", "_", "_"]
    orientation = Orientation.HORIZONTAL
    original_col = 4
    result_horizontal = blank_puzzle.trim_candidate(candidate, orientation,
                                                    0, 0, 0, original_col)
    assert (result_horizontal is None)


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
    assert (len_horizontal == length - 1 and len_vertical == length - 1)


def test_check_for_adjacency_removes_last_character(blank_puzzle):
    """Tests that function removes the first letter of a candidate if it
       touches another word in the puzzle without intersecting it"""
    blank_puzzle.grid[6][6] = "x"
    candidate1 = ["_", "_", "_", "_", "_"]
    candidate2 = candidate1[:]
    length = len(candidate1)
    (result_horizontal, x, y) = blank_puzzle.check_for_adjacency(candidate1,
                                                                 Orientation.HORIZONTAL, 6, 1)
    (result_vertical, x, y) = blank_puzzle.check_for_adjacency(candidate2,
                                                               Orientation.VERTICAL, 1, 6)
    len_horizontal = len(result_horizontal)
    len_vertical = len(result_vertical)
    assert (len_horizontal == length - 1 and len_vertical == length - 1)


def test_check_cell_is_legal_fails_for_word_running_into_parallel_word(blank_puzzle):
    """Tests that function returns false if the cell being tested will result
       in the candidate running into another word with the same orientation"""
    blank_puzzle.grid[0][4] = "x"
    blank_puzzle.letter_use[0][4] = LetterUse.ACROSS
    result = blank_puzzle.check_cell_is_legal(0, 3, 0, 4, Orientation.HORIZONTAL)
    assert (result is False)


def test_check_cell_is_legal_passes_for_occupied_cell(blank_puzzle):
    """Tests that function returns True if the cell being tested is not blank"""
    blank_puzzle.grid[4][4] = "x"
    result = blank_puzzle.check_cell_is_legal(4, 4, 5, 4, Orientation.HORIZONTAL)
    assert (result is True)


def test_check_cell_is_legal_fails_for_occupied_neighbour(blank_puzzle):
    """Tests that function returns False if either of the cells neighbouring
       it (in the orthogonal direction) are occupied"""
    blank_puzzle.grid[2][2] = "x"
    result_horizontal = blank_puzzle.check_cell_is_legal(3, 2, 4, 2, Orientation.HORIZONTAL)
    result_vertical = blank_puzzle.check_cell_is_legal(2, 3, 3, 3, Orientation.VERTICAL)
    assert (result_horizontal is False and result_vertical is False)


def test_check_cell_occupied_fails_for_out_of_bounds_cell(blank_puzzle):
    """Tests that the function returns False if the row or column
       specified are not within the crossword"""
    assert (blank_puzzle.check_cell_occupied(0, 10) is False)


def test_check_cell_occupied_returns_true_for_occupied_cell(blank_puzzle):
    """Checks that a cell that is occupied will return a True result"""
    blank_puzzle.grid[0][0] = "x"
    assert (blank_puzzle.check_cell_occupied(0, 0) is True)


def test_prune_intersection_set_removes_unusable_intersection_cell(blank_puzzle):
    """Supplied the function with a set containing one point adjacent to an 
       occupied cell, and tests that the set returned by the function is empty"""
    blank_puzzle.grid[2][2] = "x"
    intersection_hor = (2, 1, Orientation.HORIZONTAL)
    intersection_ver = (1, 2, Orientation.VERTICAL)
    blank_puzzle.intersections.add(intersection_hor)
    blank_puzzle.intersections.add(intersection_ver)
    blank_puzzle.prune_intersection_set()
    assert (len(blank_puzzle.intersections) == 0)


def test_prune_intersection_set_retains_intersections_at_edge_of_puzzle(blank_puzzle):
    """Invokes the function with an intersection at each of the 4 edges of
       the puzzle and checks that the intersection set contains the same 4
       after invocation"""
    blank_puzzle.intersections.add((0, 3, Orientation.VERTICAL))
    blank_puzzle.intersections.add((0, 6, Orientation.VERTICAL))
    blank_puzzle.intersections.add((3, 0, Orientation.HORIZONTAL))
    blank_puzzle.intersections.add((3, 6, Orientation.HORIZONTAL))
    copy_set = set(blank_puzzle.intersections)
    blank_puzzle.prune_intersection_set()
    assert (copy_set == blank_puzzle.intersections)


def test_reindex_clues_gives_same_index_to_clues_starting_in_same_cell(puzzle_w_clues):
    """Checks that clues that share the same starting cell have the same index
       after function is called. The fixture puzzle_w_clues is set up to have one 
       such pair of clues"""
    puzzle_w_clues.reindex_clues()
    index_shared = True
    for clue_a in puzzle_w_clues.clues_across:
        for clue_d in puzzle_w_clues.clues_down:
            if clue_a.start_row == clue_d.start_row and clue_a.start_col == clue_d.start_col:
                if clue_a.index != clue_d.index:
                    index_shared = False
    assert (index_shared is True)


def test_reindex_clues_gives_consecutive_indices_to_clues(puzzle_w_clues):
    """Calls function, and then checks to ensure that the clues of each orientation
       respectively are indexed from zero without missing any numbers"""
    # clue indices start at 1, as they are shown to the user
    ordinals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    puzzle_w_clues.reindex_clues()

    # create a set with the indices that should occur
    clues_across_count = len(puzzle_w_clues.clues_across)
    clues_down_count = len(puzzle_w_clues.clues_down)
    across_indices_set = set(ordinals[:clues_across_count])
    down_indices_set = set(ordinals[:clues_down_count])

    # create a set with the indices that actually occur after function call
    result_across_set = {clue.index for clue in puzzle_w_clues.clues_across}
    result_down_set = {clue.index for clue in puzzle_w_clues.clues_down}

    # assert that the sets are equal(contain same elements)
    assert (across_indices_set == result_across_set and down_indices_set == result_down_set)
