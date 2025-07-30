"""
Wordle Game Package
A Python implementation of the popular Wordle word guessing game.
"""

__version__ = "1.0.0"
__author__ = "Wordle Game Developer"
__description__ = "A Python implementation of the Wordle word guessing game"

from .game import WordleGame
from .word_scraper import WordScraper
from .word_list import WordList
from .utils import print_welcome, print_goodbye, print_guess_result

__all__ = [
    'WordleGame',
    'WordScraper', 
    'WordList',
    'print_welcome',
    'print_goodbye',
    'print_guess_result'
] 