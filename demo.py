#!/usr/bin/env python3
"""
Demo script for the Wordle game.
This script demonstrates the core functionality of the Wordle game.
"""

import sys
import os

# Add the wordle package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wordle'))

from wordle.word_list import WordList
from wordle.utils import calculate_guess_result, print_guess_result


def demo_word_validation():
    """Demonstrate word validation functionality."""
    print("🔍 Word Validation Demo")
    print("=" * 30)
    
    # Sample words
    test_words = ["about", "above", "abuse", "actor", "acute"]
    word_list = WordList(test_words)
    
    test_guesses = ["about", "hello", "world", "test", "abc", "abcdef"]
    
    for guess in test_guesses:
        is_valid = word_list.is_valid_word(guess)
        status = "✅ Valid" if is_valid else "❌ Invalid"
        print(f"'{guess}' -> {status}")
    
    print()


def demo_guess_result():
    """Demonstrate guess result calculation."""
    print("🎯 Guess Result Demo")
    print("=" * 30)
    
    target_word = "about"
    test_guesses = ["about", "abxyz", "bouta", "xyzab"]
    
    for guess in test_guesses:
        result = calculate_guess_result(guess, target_word)
        print(f"Target: {target_word.upper()}")
        print(f"Guess:  {guess.upper()}")
        print("Result: ", end="")
        print_guess_result(guess, result)
        print()


def demo_word_list_features():
    """Demonstrate word list features."""
    print("📚 Word List Features Demo")
    print("=" * 30)
    
    # Sample words
    test_words = [
        "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
        "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
        "alike", "alive", "allow", "alone", "along", "alter", "among", "anger"
    ]
    
    word_list = WordList(test_words)
    
    print(f"Total words: {word_list.get_word_count()}")
    
    # Words starting with "ab"
    ab_words = word_list.get_words_starting_with("ab")
    print(f"Words starting with 'ab': {ab_words}")
    
    # Words containing "a"
    a_words = word_list.get_words_containing_letter("a")
    print(f"Words containing 'a': {len(a_words)} words")
    
    # Pattern matching
    pattern_words = word_list.get_words_with_pattern("a??le")
    print(f"Words matching pattern 'a??le': {pattern_words}")
    
    # Most common letters
    common_letters = word_list.get_most_common_letters(5)
    print(f"Most common letters: {common_letters}")
    
    print()


def demo_game_logic():
    """Demonstrate game logic."""
    print("🎮 Game Logic Demo")
    print("=" * 30)
    
    # Sample game scenario
    target_word = "about"
    guesses = ["hello", "world", "about"]
    
    print(f"Target word: {target_word}")
    print("Guessing sequence:")
    
    for i, guess in enumerate(guesses, 1):
        result = calculate_guess_result(guess, target_word)
        won = guess == target_word
        
        print(f"\nAttempt {i}: {guess.upper()}")
        print_guess_result(guess, result)
        
        if won:
            print(f"🎉 Won in {i} attempts!")
            break
        elif i == len(guesses):
            print("😔 Game over - didn't win")
    
    print()


def main():
    """Run the demo."""
    print("🎯 WORDLE GAME DEMO")
    print("=" * 50)
    print("This demo shows the core functionality of the Wordle game.")
    print()
    
    demo_word_validation()
    demo_guess_result()
    demo_word_list_features()
    demo_game_logic()
    
    print("🎉 Demo completed!")
    print("\nTo play the full game, run: python main.py")


if __name__ == "__main__":
    main() 