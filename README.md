# Debugging an ISBN Validator

[![CI](https://github.com/sklsp/Debugging-an-ISBN-Validator/actions/workflows/ci.yml/badge.svg)](https://github.com/sklsp/Debugging-an-ISBN-Validator/actions/workflows/ci.yml)

A debugging exercise: a Python script that validates ISBN-10 and ISBN-13 check digits, shipped with several planted bugs. The point of this repo is the debugging work, not the algorithm.

## How to run

```powershell
python isbn_validator.py
```

Enter `<isbn>,<length>` at the prompt, for example `0306406152,10`.

You can also import it and call `validate_isbn(isbn, length)` directly:

```python
import isbn_validator as v
v.validate_isbn('9780306406157', 13)   # Valid ISBN Code.
v.validate_isbn('097522980X', 10)      # Valid ISBN Code. (X check digit)
```

## Bugs found and fixed

| Bug | Where | Fix |
|---|---|---|
| `len(isbn, length)` - `len()` takes one argument, so the script crashed on every input | `validate_isbn` | `len(isbn)` |
| Off-by-one slicing: main digits took all characters and the check digit read past the end of the string (IndexError) | `validate_isbn` | `isbn[0:length-1]` for main digits, `isbn[length-1]` for the check digit |
| Missing indentation under `if length == 10 or length == 13:` - a SyntaxError that stopped the file from even parsing | `main` | indented the body of both branches |
| `main()` ran on import with no guard | module bottom | wrapped in `if __name__ == '__main__':` |
| Input without a comma crashed with IndexError | `main` | prints `Enter comma-separated values.` |
| A length that is not a number crashed with ValueError | `main` | prints `Length must be a number.` |
| A letter among the digits crashed with ValueError | `validate_isbn` | prints `Invalid character was found.` |
| A lowercase `x` check digit was rejected | `validate_isbn` | compares the check digit in upper case |

## Tests

```bash
pip install pytest
python -m pytest -q
```

`tests/test_isbn_validator.py` (12 tests) feeds every kind of input through `main()`: valid ISBN-10 and ISBN-13 codes, X and x check digits, wrong check digits, a wrong length, no comma, a non-numeric length and a letter among the digits. Each gets a message, never a traceback. CI runs the tests on every push.
