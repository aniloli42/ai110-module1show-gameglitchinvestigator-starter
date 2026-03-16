import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# --- get_range_for_difficulty ---

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_range_unknown_defaults():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- parse_guess ---

def test_parse_valid_int():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_valid_float_truncates():
    ok, val, err = parse_guess("3.9")
    assert ok is True
    assert val == 3
    assert err is None

def test_parse_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_none():
    ok, val, err = parse_guess(None)
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_non_numeric():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert val is None
    assert err is not None

def test_parse_negative():
    ok, val, err = parse_guess("-5")
    assert ok is True
    assert val == -5

def test_parse_zero():
    ok, val, err = parse_guess("0")
    assert ok is True
    assert val == 0


# --- check_guess ---

def test_check_guess_correct():
    outcome, msg = check_guess(42, 42)
    assert outcome == "Win"

def test_check_guess_too_high():
    outcome, msg = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in msg

def test_check_guess_too_low():
    outcome, msg = check_guess(10, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in msg

def test_check_guess_boundary_low():
    outcome, _ = check_guess(1, 1)
    assert outcome == "Win"

def test_check_guess_boundary_high():
    outcome, _ = check_guess(100, 100)
    assert outcome == "Win"


# --- update_score ---

def test_score_win_first_attempt():
    score = update_score(0, "Win", 1)
    assert score == 80  # 100 - 10*(1+1)

def test_score_win_minimum_points():
    # attempt_number=10 → 100 - 110 = -10 → clamped to 10
    score = update_score(0, "Win", 10)
    assert score == 10

def test_score_too_high_deducts():
    score = update_score(50, "Too High", 1)
    assert score == 45

def test_score_too_low_deducts():
    score = update_score(50, "Too Low", 1)
    assert score == 45

def test_score_unknown_outcome_unchanged():
    score = update_score(50, "SomethingElse", 1)
    assert score == 50

def test_score_accumulates():
    score = update_score(0, "Too High", 1)   # 0 - 5 = -5
    score = update_score(score, "Too Low", 2) # -5 - 5 = -10
    assert score == -10
