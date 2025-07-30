#!/usr/bin/env python3
"""
Simple run script for the Wordle game.
This script provides an easy way to start the game and handle any setup.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import requests
        import bs4
        import colorama
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main function to run the Wordle game."""
    print("🎯 Wordle Game Launcher")
    print("=" * 30)
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("\n🔧 Installing missing dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install -r requirements.txt")
            return
        
        # Check again after installation
        if not check_dependencies():
            print("❌ Dependencies still missing after installation")
            return
    
    print("✅ All dependencies are installed!")
    print("\n🚀 Starting Wordle game...")
    print("=" * 30)
    
    # Import and run the main game
    try:
        from main import main as game_main
        game_main()
    except ImportError as e:
        print(f"❌ Error importing game: {e}")
        print("Make sure you're running this from the project root directory")
    except Exception as e:
        print(f"❌ Error running game: {e}")

if __name__ == "__main__":
    main() 