"""
Wordle Game Module
Main game logic for the Wordle word guessing game.
"""

import random
import json
import os
from typing import List, Dict, Optional
from .word_list import WordList
from .utils import (
    print_welcome, print_goodbye, print_guess_result, print_keyboard_hint,
    print_game_board, print_win_message, print_lose_message, print_statistics,
    get_user_input, validate_guess, calculate_guess_result, update_used_letters,
    clear_screen
)


class WordleGame:
    """Main Wordle game class."""
    
    def __init__(self, words: List[str]):
        """
        Initialize the Wordle game.
        
        Args:
            words (List[str]): List of valid 5-letter words
        """
        self.word_list = WordList(words)
        self.target_word = None
        self.guesses = []
        self.results = []
        self.used_letters = {}
        self.attempts = 0
        self.max_attempts = 6
        self.game_won = False
        self.stats_file = "data/wordle_stats.json"
        self.stats = self.load_statistics()
    
    def load_statistics(self) -> Dict:
        """
        Load game statistics from file.
        
        Returns:
            Dict: Game statistics
        """
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load statistics: {e}")
        
        # Default statistics
        return {
            'games_played': 0,
            'games_won': 0,
            'current_streak': 0,
            'max_streak': 0,
            'guess_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        }
    
    def save_statistics(self):
        """Save game statistics to file."""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"⚠️  Could not save statistics: {e}")
    
    def update_statistics(self, won: bool, attempts: int):
        """
        Update game statistics.
        
        Args:
            won (bool): Whether the game was won
            attempts (int): Number of attempts taken
        """
        self.stats['games_played'] += 1
        
        if won:
            self.stats['games_won'] += 1
            self.stats['current_streak'] += 1
            self.stats['max_streak'] = max(self.stats['max_streak'], self.stats['current_streak'])
            self.stats['guess_distribution'][attempts] += 1
        else:
            self.stats['current_streak'] = 0
        
        self.save_statistics()
    
    def start_new_game(self):
        """Start a new game with a random target word."""
        self.target_word = self.word_list.get_random_word()
        if not self.target_word:
            raise ValueError("No valid words available for the game")
        
        self.guesses = []
        self.results = []
        self.used_letters = {}
        self.attempts = 0
        self.game_won = False
        
        print(f"\n🎯 New game started! You have {self.max_attempts} attempts.")
        print(f"📝 Word list contains {self.word_list.get_word_count()} words.")
    
    def get_guess(self) -> Optional[str]:
        """
        Get a valid guess from the user.
        
        Returns:
            Optional[str]: Valid guess or None if user wants to quit
        """
        while True:
            guess = get_user_input(f"Enter your guess ({self.attempts + 1}/{self.max_attempts}): ").lower()
            
            if guess in ['quit', 'exit', 'q']:
                return None
            
            is_valid, error_msg = validate_guess(guess, self.word_list)
            
            if is_valid:
                return guess
            else:
                print(f"❌ {error_msg}")
    
    def process_guess(self, guess: str) -> bool:
        """
        Process a guess and return whether the game is won.
        
        Args:
            guess (str): The guessed word
            
        Returns:
            bool: True if the game is won, False otherwise
        """
        self.guesses.append(guess)
        self.attempts += 1
        
        # Calculate result
        result = calculate_guess_result(guess, self.target_word)
        self.results.append(result)
        
        # Update used letters
        self.used_letters = update_used_letters(guess, result, self.used_letters)
        
        # Check if won
        if guess == self.target_word:
            self.game_won = True
            return True
        
        return False
    
    def display_game_state(self):
        """Display the current game state."""
        clear_screen()
        print_game_board(self.guesses, self.results)
        print_keyboard_hint(self.used_letters)
    
    def play_round(self) -> bool:
        """
        Play one round of the game.
        
        Returns:
            bool: True if game should continue, False if should end
        """
        self.display_game_state()
        
        guess = self.get_guess()
        if guess is None:
            print("\n👋 Game ended by user.")
            return False
        
        won = self.process_guess(guess)
        
        if won:
            self.display_game_state()
            print_win_message(self.attempts)
            self.update_statistics(True, self.attempts)
            return False
        
        if self.attempts >= self.max_attempts:
            self.display_game_state()
            print_lose_message(self.target_word)
            self.update_statistics(False, self.attempts)
            return False
        
        return True
    
    def play(self):
        """Main game loop."""
        try:
            while True:
                self.start_new_game()
                
                # Main game loop
                while self.attempts < self.max_attempts and not self.game_won:
                    if not self.play_round():
                        break
                
                # Ask if player wants to play again
                print_statistics(self.stats)
                
                play_again = get_user_input("\nPlay again? (y/n): ").lower()
                if play_again not in ['y', 'yes', 'yeah', 'sure']:
                    break
                
                print("\n" + "=" * 50)
        
        except KeyboardInterrupt:
            print("\n\n👋 Game interrupted. Goodbye!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
    
    def get_hint(self) -> str:
        """
        Get a hint for the current word.
        
        Returns:
            str: A hint about the word
        """
        if not self.target_word:
            return "No game in progress."
        
        # Provide different types of hints based on game state
        if self.attempts == 0:
            # First guess - give a general hint
            first_letter = self.target_word[0]
            return f"The word starts with '{first_letter.upper()}'."
        
        elif self.attempts < 3:
            # Early game - give letter frequency hint
            common_letters = self.word_list.get_most_common_letters(5)
            return f"Common letters in 5-letter words: {', '.join([letter.upper() for letter, _ in common_letters])}"
        
        else:
            # Late game - give pattern hint
            # Find a word that matches some known pattern
            known_letters = []
            for i, result in enumerate(self.results[-1]):
                if result == 'correct':
                    known_letters.append((i, self.guesses[-1][i]))
            
            if known_letters:
                pattern = ['?'] * 5
                for pos, letter in known_letters:
                    pattern[pos] = letter
                
                matching_words = self.word_list.get_words_with_pattern(''.join(pattern))
                if matching_words:
                    return f"Words matching current pattern: {', '.join(matching_words[:3])}"
            
            return "Keep trying! Use the colored feedback to guide your next guess."
    
    def show_help(self):
        """Show help information."""
        print("\n" + "=" * 50)
        print("🎯 WORDLE HELP 🎯")
        print("=" * 50)
        print("• Guess the 5-letter word in 6 attempts")
        print("• After each guess, letters are colored:")
        print("  🟩 Green: Letter is correct and in right position")
        print("  🟨 Yellow: Letter is correct but in wrong position")
        print("  ⬜ Gray: Letter is not in the word")
        print("• Commands:")
        print("  - Type 'quit', 'exit', or 'q' to end the game")
        print("  - Type 'hint' for a hint")
        print("  - Type 'help' to show this message")
        print("• Tips:")
        print("  - Start with common letters like E, A, R, T")
        print("  - Use the keyboard display to track used letters")
        print("  - Pay attention to letter positions from previous guesses")
        print("=" * 50)
    
    def get_game_info(self) -> Dict:
        """
        Get current game information.
        
        Returns:
            Dict: Game information
        """
        return {
            'target_word': self.target_word,
            'attempts': self.attempts,
            'max_attempts': self.max_attempts,
            'guesses': self.guesses,
            'results': self.results,
            'used_letters': self.used_letters,
            'game_won': self.game_won,
            'word_count': self.word_list.get_word_count()
        } 