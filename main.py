#!/usr/bin/env python3
"""
Wordle Game - Main Entry Point
A Python implementation of the popular Wordle word guessing game.
"""

import sys
import os

# Add the wordle package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wordle'))

from wordle.game import WordleGame
from wordle.word_scraper import WordScraper
from wordle.utils import print_welcome, print_goodbye


def main():
    """Main function to run the Wordle game."""
    try:
        # Print welcome message
        print_welcome()
        
        # Initialize word scraper and get words
        scraper = WordScraper()
        words = scraper.get_words()
        
        if not words:
            print("❌ Error: Could not load word list. Please check your internet connection.")
            return
        
        # Create and start the game
        game = WordleGame(words)
        game.play()
        
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        print_goodbye()


if __name__ == "__main__":
    main() 