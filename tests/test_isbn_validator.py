import pytest

import isbn_validator as v


def run_main(monkeypatch, capsys, typed):
    monkeypatch.setattr("builtins.input", lambda prompt="": typed)
    v.main()
    return capsys.readouterr().out.strip()


@pytest.mark.parametrize("typed, expected", [
    ("0306406152,10", "Valid ISBN Code."),
    ("9780306406157,13", "Valid ISBN Code."),
    ("097522980X,10", "Valid ISBN Code."),
    ("097522980x,10", "Valid ISBN Code."),          # a lowercase x check digit
    ("0306406153,10", "Invalid ISBN Code."),
    ("9780306406158,13", "Invalid ISBN Code."),
    ("030640615,10", "ISBN-10 code should be 10 digits long."),
    ("0306406152,12", "Length should be 10 or 13."),
    ("0306406152", "Enter comma-separated values."),
    ("0306406152,ten", "Length must be a number."),
    ("03A6406152,10", "Invalid character was found."),
])
def test_every_input_gets_a_message_not_a_crash(monkeypatch, capsys, typed, expected):
    assert run_main(monkeypatch, capsys, typed) == expected


def test_check_digits():
    assert v.calculate_check_digit_10([0, 3, 0, 6, 4, 0, 6, 1, 5]) == "2"
    assert v.calculate_check_digit_10([0, 9, 7, 5, 2, 2, 9, 8, 0]) == "X"
    assert v.calculate_check_digit_13([9, 7, 8, 0, 3, 0, 6, 4, 0, 6, 1, 5]) == "7"
