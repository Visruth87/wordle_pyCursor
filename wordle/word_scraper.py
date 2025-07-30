"""
Word Scraper Module
Handles scraping of 5-letter words from the Word Unscrambler website.
"""

import requests
from bs4 import BeautifulSoup
import re
import os
from typing import List, Optional


class WordScraper:
    """Scrapes 5-letter words from the Word Unscrambler website."""
    
    def __init__(self, url: str = "https://www.wordunscrambler.net/word-list/wordle-word-list"):
        """
        Initialize the word scraper.
        
        Args:
            url (str): The URL to scrape words from
        """
        self.url = url
        self.data_file = "data/words.txt"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_words(self) -> List[str]:
        """
        Scrape 5-letter words from the website.
        
        Returns:
            List[str]: List of 5-letter words
        """
        try:
            print("🌐 Scraping words from the web...")
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all list items that contain 5-letter words
            words = []
            
            # Look for words in list items
            list_items = soup.find_all('li')
            for item in list_items:
                text = item.get_text().strip()
                # Check if it's a 5-letter word (only letters, exactly 5 characters)
                if re.match(r'^[a-zA-Z]{5}$', text):
                    words.append(text.lower())
            
            # If no words found in list items, try other patterns
            if not words:
                # Look for words in paragraphs or other text elements
                text_elements = soup.find_all(['p', 'div', 'span'])
                for element in text_elements:
                    text = element.get_text()
                    # Find all 5-letter words in the text
                    found_words = re.findall(r'\b[a-zA-Z]{5}\b', text)
                    words.extend([word.lower() for word in found_words])
            
            # Remove duplicates and sort
            words = sorted(list(set(words)))
            
            print(f"✅ Successfully scraped {len(words)} words")
            return words
            
        except requests.RequestException as e:
            print(f"❌ Error scraping words: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected error while scraping: {e}")
            return []
    
    def load_cached_words(self) -> List[str]:
        """
        Load words from cached file if it exists.
        
        Returns:
            List[str]: List of words from cache, or empty list if file doesn't exist
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    words = [line.strip() for line in f if line.strip()]
                print(f"📁 Loaded {len(words)} words from cache")
                return words
            return []
        except Exception as e:
            print(f"❌ Error loading cached words: {e}")
            return []
    
    def save_words_to_cache(self, words: List[str]) -> bool:
        """
        Save words to cache file.
        
        Args:
            words (List[str]): List of words to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                for word in words:
                    f.write(word + '\n')
            
            print(f"💾 Saved {len(words)} words to cache")
            return True
        except Exception as e:
            print(f"❌ Error saving words to cache: {e}")
            return False
    
    def get_words(self) -> List[str]:
        """
        Get words from cache or scrape from web.
        
        Returns:
            List[str]: List of 5-letter words
        """
        # Try to load from cache first
        words = self.load_cached_words()
        
        # If cache is empty or has too few words, scrape from web
        if len(words) < 100:  # Arbitrary threshold
            print("🔄 Cache is empty or incomplete, scraping from web...")
            words = self.scrape_words()
            
            if words:
                # Save to cache for future use
                self.save_words_to_cache(words)
            else:
                # If scraping failed, try to use fallback words
                print("⚠️  Scraping failed, using fallback word list...")
                words = self.get_fallback_words()
        
        return words
    
    def get_fallback_words(self) -> List[str]:
        """
        Get a fallback list of common 5-letter words.
        
        Returns:
            List[str]: List of fallback 5-letter words
        """
        fallback_words = [
            "about", "above", "abuse", "actor", "acute", "admit", "adopt", "adult",
            "after", "again", "agent", "agree", "ahead", "alarm", "album", "alert",
            "alike", "alive", "allow", "alone", "along", "alter", "among", "anger",
            "angle", "angry", "apart", "apple", "apply", "arena", "argue", "arise",
            "array", "aside", "asset", "audio", "audit", "avoid", "award", "aware",
            "badly", "baker", "bases", "basic", "beach", "began", "begin", "begun",
            "being", "below", "bench", "billy", "birth", "black", "blame", "blank",
            "blind", "block", "blood", "board", "boost", "booth", "bound", "brain",
            "brand", "bread", "break", "breed", "brief", "bring", "broad", "broke",
            "brown", "build", "built", "buyer", "cable", "calif", "carry", "catch",
            "cause", "chain", "chair", "chart", "chase", "cheap", "check", "chest",
            "chief", "child", "china", "chose", "civil", "claim", "class", "clean",
            "clear", "click", "clock", "close", "coach", "coast", "could", "count",
            "court", "cover", "craft", "crash", "cream", "crime", "cross", "crowd",
            "crown", "crude", "crush", "curve", "cycle", "daily", "dance", "dated",
            "dealt", "death", "debut", "delay", "depth", "doing", "doubt", "dozen",
            "draft", "drama", "drank", "draw", "dress", "drill", "drink", "drive",
            "drove", "dying", "eager", "early", "earth", "eight", "elite", "empty",
            "enemy", "enjoy", "enter", "entry", "equal", "error", "event", "every",
            "exact", "exist", "extra", "faith", "false", "fault", "fiber", "field",
            "fifth", "fifty", "fight", "final", "first", "fixed", "flash", "fleet",
            "floor", "fluid", "focus", "force", "forth", "forty", "forum", "found",
            "frame", "frank", "fraud", "fresh", "front", "fruit", "fully", "funny",
            "giant", "given", "glass", "globe", "going", "grace", "grade", "grand",
            "grant", "grass", "grave", "great", "green", "gross", "group", "grown",
            "guard", "guess", "guest", "guide", "happy", "harry", "heart", "heavy",
            "hence", "henry", "horse", "hotel", "house", "human", "ideal", "image",
            "index", "inner", "input", "issue", "japan", "jimmy", "joint", "jones",
            "judge", "known", "label", "large", "laser", "later", "laugh", "layer",
            "learn", "lease", "least", "leave", "legal", "level", "lewis", "light",
            "limit", "links", "lives", "local", "loose", "lower", "lucky", "lunch",
            "lying", "magic", "major", "maker", "march", "maria", "match", "maybe",
            "mayor", "meant", "media", "metal", "might", "minor", "minus", "mixed",
            "model", "money", "month", "moral", "motor", "mount", "mouse", "mouth",
            "moved", "movie", "music", "needs", "never", "newly", "night", "noise",
            "north", "noted", "novel", "nurse", "occur", "ocean", "offer", "often",
            "order", "other", "ought", "paint", "panel", "paper", "party", "peace",
            "peter", "phase", "phone", "photo", "piece", "pilot", "pitch", "place",
            "plain", "plane", "plant", "plate", "point", "pound", "power", "press",
            "price", "pride", "prime", "print", "prior", "prize", "proof", "proud",
            "prove", "queen", "quick", "quiet", "quite", "radio", "raise", "range",
            "rapid", "ratio", "reach", "ready", "realm", "rebel", "refer", "relax",
            "reply", "right", "rival", "river", "robin", "roger", "roman", "rough",
            "round", "route", "royal", "rural", "scale", "scene", "scope", "score",
            "sense", "serve", "seven", "shall", "shape", "share", "sharp", "sheet",
            "shelf", "shell", "shift", "shirt", "shock", "shoot", "short", "shown",
            "sight", "since", "sixth", "sixty", "sized", "skill", "sleep", "slide",
            "small", "smart", "smile", "smith", "smoke", "solid", "solve", "sorry",
            "sound", "south", "space", "spare", "speak", "speed", "spend", "spent",
            "split", "spoke", "sport", "staff", "stage", "stake", "stand", "start",
            "state", "steam", "steel", "steep", "steer", "stern", "steve", "stick",
            "still", "stock", "stone", "stood", "store", "storm", "story", "strip",
            "stuck", "study", "stuff", "style", "sugar", "suite", "super", "sweet",
            "table", "taken", "taste", "taxes", "teach", "teeth", "terry", "texas",
            "thank", "theft", "their", "theme", "there", "these", "thick", "thing",
            "think", "third", "those", "three", "threw", "throw", "thumb", "tiger",
            "tight", "timer", "title", "today", "topic", "total", "touch", "tough",
            "tower", "track", "trade", "train", "treat", "trend", "trial", "tribe",
            "trick", "tried", "tries", "truck", "truly", "trunk", "trust", "truth",
            "twice", "under", "undue", "union", "unity", "until", "upper", "upset",
            "urban", "usage", "usher", "using", "usual", "valid", "value", "video",
            "virus", "visit", "vital", "vocal", "voice", "waste", "watch", "water",
            "wheel", "where", "which", "while", "white", "whole", "whose", "woman",
            "women", "world", "worry", "worse", "worst", "worth", "would", "wound",
            "write", "wrong", "wrote", "yield", "young", "youth"
        ]
        return fallback_words 