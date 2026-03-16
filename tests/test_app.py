import pytest
from streamlit.testing.v1 import AppTest


APP = "app.py"


def fresh():
    """Return a freshly run AppTest instance."""
    return AppTest.from_file(APP).run()


# --- Initial state ---

def test_initial_status_is_playing():
    at = fresh()
    assert at.session_state["status"] == "playing"

def test_initial_attempts_is_zero():
    at = fresh()
    assert at.session_state["attempts"] == 0

def test_initial_score_is_zero():
    at = fresh()
    assert at.session_state["score"] == 0

def test_initial_secret_within_normal_range():
    at = fresh()
    secret = at.session_state["secret"]
    assert 1 <= secret <= 100  # Normal difficulty default


# --- Difficulty switch regenerates secret ---

def test_secret_regenerates_on_difficulty_change():
    at = fresh()
    # Default is Normal (index=1). Switch to Easy (index=0).
    at.sidebar.selectbox[0].set_value("Easy").run()
    secret = at.session_state["secret"]
    assert 1 <= secret <= 20

def test_attempts_reset_on_difficulty_change():
    at = fresh()
    # Manually set some attempts then switch difficulty
    at.session_state["attempts"] = 3
    at.sidebar.selectbox[0].set_value("Hard").run()
    assert at.session_state["attempts"] == 0


# --- Submitting a guess ---

def test_submit_invalid_guess_not_added_to_history():
    at = fresh()
    at.text_input[0].set_value("abc")
    at.button[0].click().run()
    assert at.session_state["history"] == []

def test_submit_invalid_guess_does_not_increment_attempts():
    at = fresh()
    at.text_input[0].set_value("abc")
    at.button[0].click().run()
    assert at.session_state["attempts"] == 0

def test_submit_valid_guess_increments_attempts():
    at = fresh()
    secret = at.session_state["secret"]
    # Guess something that is definitely not the secret
    guess = secret + 1 if secret < 100 else secret - 1
    at.text_input[0].set_value(str(guess))
    at.button[0].click().run()
    assert at.session_state["attempts"] == 1

def test_submit_correct_guess_sets_won():
    at = fresh()
    secret = at.session_state["secret"]
    at.text_input[0].set_value(str(secret))
    at.button[0].click().run()
    assert at.session_state["status"] == "won"

def test_win_updates_score():
    at = fresh()
    secret = at.session_state["secret"]
    at.text_input[0].set_value(str(secret))
    at.button[0].click().run()
    assert at.session_state["score"] > 0


# --- Attempt limit ---

def test_game_lost_after_max_attempts():
    at = fresh()
    # Switch to Hard (5 attempts, range 1–50)
    at.sidebar.selectbox[0].set_value("Hard").run()
    secret = at.session_state["secret"]
    wrong = 1 if secret != 1 else 2

    for _ in range(5):
        at.text_input[0].set_value(str(wrong))
        at.button[0].click().run()
        if at.session_state["status"] == "lost":
            break

    assert at.session_state["status"] == "lost"


# --- New Game button ---

def test_new_game_resets_attempts():
    at = fresh()
    at.session_state["attempts"] = 4
    at.button[1].click().run()  # New Game button
    assert at.session_state["attempts"] == 0

def test_new_game_resets_status():
    at = fresh()
    at.session_state["status"] = "lost"
    at.button[1].click().run()
    assert at.session_state["status"] == "playing"

def test_new_game_generates_new_secret_in_range():
    at = fresh()
    at.button[1].click().run()
    secret = at.session_state["secret"]
    assert 1 <= secret <= 100  # Normal difficulty
