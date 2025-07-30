# Wordle Game

A Python implementation of the popular Wordle word guessing game.

## Description

Wordle is a word guessing game where players have six attempts to guess a five-letter word. After each guess, the game provides feedback:
- 🟩 Green: Letter is correct and in the right position
- 🟨 Yellow: Letter is correct but in the wrong position  
- ⬜ Gray: Letter is not in the word

## Features

- Complete Wordle game implementation
- Automatic word list scraping from [Word Unscrambler](https://www.wordunscrambler.net/word-list/wordle-word-list)
- Beautiful terminal-based interface with colored output
- Word validation and feedback system
- Game statistics tracking
- Easy to use and extend

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd wordle-game
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the game:
```bash
python main.py
```

## Game Rules

1. You have 6 attempts to guess the 5-letter word
2. After each guess, you'll see:
   - 🟩 Green squares for correct letters in correct positions
   - 🟨 Yellow squares for correct letters in wrong positions
   - ⬜ Gray squares for letters not in the word
3. Use the feedback to make your next guess
4. Try to guess the word before running out of attempts!

## Project Structure

```
wordle-game/
├── README.md
├── requirements.txt
├── main.py
├── wordle/
│   ├── __init__.py
│   ├── game.py
│   ├── word_scraper.py
│   ├── word_list.py
│   └── utils.py
├── data/
│   └── words.txt
└── tests/
    ├── __init__.py
    └── test_game.py
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Word list sourced from [Word Unscrambler](https://www.wordunscrambler.net/word-list/wordle-word-list)
- Inspired by the original Wordle game 