"""
Word List Module
Manages the list of valid 5-letter words and provides word validation.
"""

from typing import List, Set, Optional
import random


class WordList:
    """Manages a list of valid 5-letter words for the Wordle game."""
    
    def __init__(self, words: List[str]):
        """
        Initialize the word list.
        
        Args:
            words (List[str]): List of 5-letter words
        """
        self.words = [word.lower().strip() for word in words if self._is_valid_word(word)]
        self.word_set = set(self.words)
        self._validate_word_list()
    
    def _is_valid_word(self, word: str) -> bool:
        """
        Check if a word is valid (5 letters, only alphabetic characters).
        
        Args:
            word (str): Word to validate
            
        Returns:
            bool: True if word is valid, False otherwise
        """
        if not word or not isinstance(word, str):
            return False
        
        word = word.lower().strip()
        return len(word) == 5 and word.isalpha()
    
    def _validate_word_list(self):
        """Validate the word list and remove invalid words."""
        original_count = len(self.words)
        self.words = [word for word in self.words if self._is_valid_word(word)]
        self.word_set = set(self.words)
        
        if len(self.words) != original_count:
            print(f"⚠️  Removed {original_count - len(self.words)} invalid words from the list")
    
    def get_random_word(self) -> Optional[str]:
        """
        Get a random word from the list.
        
        Returns:
            Optional[str]: Random word or None if list is empty
        """
        if not self.words:
            return None
        return random.choice(self.words)
    
    def is_valid_word(self, word: str) -> bool:
        """
        Check if a word is in the valid word list.
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if word is valid, False otherwise
        """
        if not self._is_valid_word(word):
            return False
        return word.lower().strip() in self.word_set
    
    def get_word_count(self) -> int:
        """
        Get the number of words in the list.
        
        Returns:
            int: Number of words
        """
        return len(self.words)
    
    def get_words_starting_with(self, prefix: str) -> List[str]:
        """
        Get all words starting with a given prefix.
        
        Args:
            prefix (str): Prefix to search for
            
        Returns:
            List[str]: List of words starting with the prefix
        """
        prefix = prefix.lower()
        return [word for word in self.words if word.startswith(prefix)]
    
    def get_words_containing_letter(self, letter: str) -> List[str]:
        """
        Get all words containing a specific letter.
        
        Args:
            letter (str): Letter to search for
            
        Returns:
            List[str]: List of words containing the letter
        """
        letter = letter.lower()
        return [word for word in self.words if letter in word]
    
    def get_words_with_pattern(self, pattern: str) -> List[str]:
        """
        Get words matching a pattern (use '?' for unknown letters).
        
        Args:
            pattern (str): Pattern to match (e.g., "a??le")
            
        Returns:
            List[str]: List of words matching the pattern
        """
        if len(pattern) != 5:
            return []
        
        pattern = pattern.lower()
        matching_words = []
        
        for word in self.words:
            if len(word) != 5:
                continue
            
            match = True
            for i, char in enumerate(pattern):
                if char != '?' and word[i] != char:
                    match = False
                    break
            
            if match:
                matching_words.append(word)
        
        return matching_words
    
    def get_sample_words(self, count: int = 10) -> List[str]:
        """
        Get a sample of words from the list.
        
        Args:
            count (int): Number of words to return
            
        Returns:
            List[str]: Sample of words
        """
        if count >= len(self.words):
            return self.words.copy()
        return random.sample(self.words, count)
    
    def get_word_frequency(self) -> dict:
        """
        Get the frequency of each letter in the word list.
        
        Returns:
            dict: Dictionary with letter frequencies
        """
        frequency = {}
        for word in self.words:
            for letter in word:
                frequency[letter] = frequency.get(letter, 0) + 1
        return frequency
    
    def get_most_common_letters(self, count: int = 10) -> List[tuple]:
        """
        Get the most common letters in the word list.
        
        Args:
            count (int): Number of letters to return
            
        Returns:
            List[tuple]: List of (letter, frequency) tuples
        """
        frequency = self.get_word_frequency()
        sorted_letters = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        return sorted_letters[:count]
    
    def __len__(self) -> int:
        """Return the number of words in the list."""
        return len(self.words)
    
    def __contains__(self, word: str) -> bool:
        """Check if a word is in the list."""
        return self.is_valid_word(word)
    
    def __iter__(self):
        """Iterate over the words in the list."""
        return iter(self.words) 