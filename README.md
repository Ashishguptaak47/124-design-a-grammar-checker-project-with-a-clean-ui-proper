# Grammar & Style Checker App

A modern, lightweight desktop Grammar, Spelling, and Style Checker built in Python. Features real-time rule matching, passive voice detection, article misuse detection, homophone correction, readability scoring, and an interactive side-by-side UI.

## Features
- **Grammar & Punctuation Engine**: Detects missing spaces after punctuation, capitalization issues, double words, and misused articles (`a apple` vs `an apple`).
- **Homophone & Phrase Correction**: Flags common mistakes like `could of`, `your welcome`, and `their going`.
- **Style & Passive Voice**: Identifies passive voice structures and overly long sentences.
- **Readability Stats**: Calculates Flesch Reading Ease score, word count, character count, and sentence count.
- **Interactive GUI**: Native Tkinter interface with issue highlights, quick-fix suggestions, and real-time statistics.

## Project Structure
```
. 
├── grammar_checker/
│   ├── __init__.py
│   ├── engine.py       # Core NLP & Grammar checking logic
│   └── ui.py           # Tkinter GUI implementation
├── tests/
│   └── test_main.py    # Unit test suite
├── main.py             # Application entry point
├── requirements.txt    # Dependencies
└── README.md
```

## Quickstart

1. **Prerequisites**: Python 3.8+
2. **Run Application**:
   ```bash
   python main.py
   ```
3. **Run Unit Tests**:
   ```bash
   python -m unittest discover tests
   ```
