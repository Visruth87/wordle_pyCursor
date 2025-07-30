"""
Test cases for the Wordle game.
"""

import unittest
import sys
import os

# Add the parent directory to the path to import the wordle package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from wordle.word_list import WordList
from wordle.utils import validate_guess, calculate_guess_result, update_used_letters


class TestWordList(unittest.TestCase):
    """Test cases for the WordList class."""
    
    def setUp(self):
        """Set up test data."""
        self.test_words = [
            "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
            "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
            "alike", "alive", "allow", "alone", "along", "alter", "among", "anger"
        ]
        self.word_list = WordList(self.test_words)
    
    def test_valid_word_validation(self):
        """Test that valid words are accepted."""
        self.assertTrue(self.word_list.is_valid_word("about"))
        self.assertTrue(self.word_list.is_valid_word("ALIVE"))
        self.assertTrue(self.word_list.is_valid_word("  actor  "))
    
    def test_invalid_word_validation(self):
        """Test that invalid words are rejected."""
        self.assertFalse(self.word_list.is_valid_word(""))
        self.assertFalse(self.word_list.is_valid_word("abc"))
        self.assertFalse(self.word_list.is_valid_word("abcdef"))
        self.assertFalse(self.word_list.is_valid_word("ab0ut"))
        self.assertFalse(self.word_list.is_valid_word("ab out"))
        self.assertFalse(self.word_list.is_valid_word("notinlist"))
    
    def test_get_random_word(self):
        """Test getting a random word."""
        word = self.word_list.get_random_word()
        self.assertIsNotNone(word)
        self.assertIn(word, self.test_words)
    
    def test_word_count(self):
        """Test word count functionality."""
        self.assertEqual(self.word_list.get_word_count(), len(self.test_words))
    
    def test_words_starting_with(self):
        """Test finding words starting with a prefix."""
        words = self.word_list.get_words_starting_with("ab")
        expected = ["about", "above", "abuse"]
        self.assertEqual(set(words), set(expected))
    
    def test_words_containing_letter(self):
        """Test finding words containing a letter."""
        words = self.word_list.get_words_containing_letter("x")
        self.assertEqual(len(words), 0)  # No words with 'x' in test data
        
        words = self.word_list.get_words_containing_letter("a")
        self.assertGreater(len(words), 0)
    
    def test_words_with_pattern(self):
        """Test finding words matching a pattern."""
        words = self.word_list.get_words_with_pattern("a??le")
        self.assertIn("alike", words)
        
        words = self.word_list.get_words_with_pattern("?????")
        self.assertEqual(len(words), len(self.test_words))
    
    def test_word_frequency(self):
        """Test letter frequency calculation."""
        frequency = self.word_list.get_word_frequency()
        self.assertIsInstance(frequency, dict)
        self.assertGreater(len(frequency), 0)
    
    def test_most_common_letters(self):
        """Test finding most common letters."""
        common_letters = self.word_list.get_most_common_letters(5)
        self.assertEqual(len(common_letters), 5)
        self.assertIsInstance(common_letters[0], tuple)
        self.assertEqual(len(common_letters[0]), 2)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test data."""
        self.test_words = ["about", "above", "abuse", "actor", "acute"]
        self.word_list = WordList(self.test_words)
    
    def test_validate_guess_valid(self):
        """Test validation of valid guesses."""
        is_valid, error_msg = validate_guess("about", self.word_list)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_validate_guess_invalid(self):
        """Test validation of invalid guesses."""
        # Empty guess
        is_valid, error_msg = validate_guess("", self.word_list)
        self.assertFalse(is_valid)
        self.assertIn("Please enter a word", error_msg)
        
        # Too short
        is_valid, error_msg = validate_guess("abc", self.word_list)
        self.assertFalse(is_valid)
        self.assertIn("exactly 5 letters", error_msg)
        
        # Too long
        is_valid, error_msg = validate_guess("abcdef", self.word_list)
        self.assertFalse(is_valid)
        self.assertIn("exactly 5 letters", error_msg)
        
        # Non-alphabetic
        is_valid, error_msg = validate_guess("ab0ut", self.word_list)
        self.assertFalse(is_valid)
        self.assertIn("only letters", error_msg)
        
        # Not in word list
        is_valid, error_msg = validate_guess("notin", self.word_list)
        self.assertFalse(is_valid)
        self.assertIn("not found", error_msg)
    
    def test_calculate_guess_result(self):
        """Test guess result calculation."""
        # Perfect match
        result = calculate_guess_result("about", "about")
        self.assertEqual(result, ["correct"] * 5)
        
        # No match
        result = calculate_guess_result("xyzab", "about")
        self.assertEqual(result, ["not_in_word"] * 5)
        
        # Partial match
        result = calculate_guess_result("abxyz", "about")
        expected = ["correct", "correct", "not_in_word", "not_in_word", "not_in_word"]
        self.assertEqual(result, expected)
        
        # Letter in wrong position
        result = calculate_guess_result("bouta", "about")
        expected = ["wrong_position", "wrong_position", "wrong_position", "wrong_position", "wrong_position"]
        self.assertEqual(result, expected)
        
        # Mixed case
        result = calculate_guess_result("abxyz", "about")
        expected = ["correct", "correct", "not_in_word", "not_in_word", "not_in_word"]
        self.assertEqual(result, expected)
    
    def test_update_used_letters(self):
        """Test updating used letters dictionary."""
        used_letters = {}
        
        # Test adding new letters
        result = ["correct", "wrong_position", "not_in_word", "not_in_word", "not_in_word"]
        updated = update_used_letters("abxyz", result, used_letters)
        self.assertEqual(updated["A"], "correct")
        self.assertEqual(updated["B"], "wrong_position")
        self.assertEqual(updated["X"], "not_in_word")
        self.assertEqual(updated["Y"], "not_in_word")
        self.assertEqual(updated["Z"], "not_in_word")
        
        # Test upgrading letter status
        result = ["wrong_position", "correct", "not_in_word", "not_in_word", "not_in_word"]
        updated = update_used_letters("baxyz", result, updated)
        self.assertEqual(updated["A"], "correct")  # Should upgrade from wrong_position
        self.assertEqual(updated["B"], "correct")  # Should upgrade from wrong_position
        self.assertEqual(updated["X"], "not_in_word")  # Should not upgrade


class TestGameLogic(unittest.TestCase):
    """Test cases for game logic."""
    
    def test_word_list_initialization(self):
        """Test that word list is properly initialized."""
        test_words = ["about", "above", "abuse"]
        word_list = WordList(test_words)
        self.assertEqual(len(word_list), 3)
        self.assertTrue("about" in word_list)
        self.assertFalse("invalid" in word_list)
    
    def test_word_list_filtering(self):
        """Test that invalid words are filtered out."""
        mixed_words = ["about", "abc", "above", "12345", "abuse", ""]
        word_list = WordList(mixed_words)
        self.assertEqual(len(word_list), 3)  # Only valid 5-letter words
        self.assertTrue("about" in word_list)
        self.assertFalse("abc" in word_list)
        self.assertFalse("12345" in word_list)


if __name__ == "__main__":
    unittest.main() 