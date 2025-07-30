#!/usr/bin/env python3
"""
Test script for the word scraper functionality.
This script tests the word scraper to ensure it can properly scrape words from the website.
"""

import sys
import os

# Add the wordle package to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'wordle'))

from wordle.word_scraper import WordScraper


def test_scraper():
    """Test the word scraper functionality."""
    print("🧪 Testing Word Scraper...")
    print("=" * 50)
    
    scraper = WordScraper()
    
    # Test getting words
    print("📥 Getting words...")
    words = scraper.get_words()
    
    if words:
        print(f"✅ Successfully loaded {len(words)} words")
        print(f"📝 Sample words: {', '.join(words[:10])}")
        
        # Test word validation
        valid_words = [word for word in words if len(word) == 5 and word.isalpha()]
        print(f"✅ Valid 5-letter words: {len(valid_words)}")
        
        if len(valid_words) > 0:
            print(f"📝 Sample valid words: {', '.join(valid_words[:10])}")
        
        # Test word list functionality
        from wordle.word_list import WordList
        word_list = WordList(words)
        print(f"📊 Word list contains {word_list.get_word_count()} valid words")
        
        # Test random word selection
        random_word = word_list.get_random_word()
        if random_word:
            print(f"🎲 Random word: {random_word}")
        
        # Test word validation
        test_words = ["about", "hello", "world", "test", "invalid"]
        print("\n🔍 Testing word validation:")
        for word in test_words:
            is_valid = word_list.is_valid_word(word)
            status = "✅" if is_valid else "❌"
            print(f"  {status} '{word}' -> {is_valid}")
        
        return True
    else:
        print("❌ Failed to load words")
        return False


if __name__ == "__main__":
    success = test_scraper()
    if success:
        print("\n🎉 Word scraper test completed successfully!")
    else:
        print("\n💥 Word scraper test failed!")
        sys.exit(1) 