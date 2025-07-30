"""
Utility functions for the Wordle game.
Provides colored output and display functions.
"""

import os
from colorama import init, Fore, Back, Style
from typing import List, Tuple

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def print_welcome():
    """Print the welcome message for the Wordle game."""
    print("\n" + "=" * 50)
    print(f"{Fore.CYAN}{Style.BRIGHT}🎯 WELCOME TO WORDLE! 🎯{Style.RESET_ALL}")
    print("=" * 50)
    print(f"{Fore.YELLOW}Guess the 5-letter word in 6 attempts!")
    print("After each guess, you'll see:")
    print(f"{Fore.GREEN}🟩 Green{Style.RESET_ALL} - Letter is correct and in the right position")
    print(f"{Fore.YELLOW}🟨 Yellow{Style.RESET_ALL} - Letter is correct but in the wrong position")
    print(f"{Fore.WHITE}⬜ Gray{Style.RESET_ALL} - Letter is not in the word")
    print("=" * 50 + "\n")


def print_goodbye():
    """Print the goodbye message."""
    print(f"\n{Fore.CYAN}Thanks for playing Wordle! 👋{Style.RESET_ALL}")


def print_guess_result(guess: str, result: List[str]):
    """
    Print the result of a guess with colored squares.
    
    Args:
        guess (str): The guessed word
        result (List[str]): List of result indicators ('correct', 'wrong_position', 'not_in_word')
    """
    print("  ", end="")
    for i, (letter, status) in enumerate(zip(guess.upper(), result)):
        if status == 'correct':
            print(f"{Back.GREEN}{Fore.BLACK} {letter} {Style.RESET_ALL}", end=" ")
        elif status == 'wrong_position':
            print(f"{Back.YELLOW}{Fore.BLACK} {letter} {Style.RESET_ALL}", end=" ")
        else:  # not_in_word
            print(f"{Back.WHITE}{Fore.BLACK} {letter} {Style.RESET_ALL}", end=" ")
    print()


def print_keyboard_hint(used_letters: dict):
    """
    Print a keyboard hint showing used letters.
    
    Args:
        used_letters (dict): Dictionary with letter status ('correct', 'wrong_position', 'not_in_word')
    """
    keyboard_layout = [
        "QWERTYUIOP",
        " ASDFGHJKL ",
        "  ZXCVBNM   "
    ]
    
    print(f"\n{Fore.CYAN}Keyboard:{Style.RESET_ALL}")
    for row in keyboard_layout:
        print("  ", end="")
        for letter in row:
            if letter == " ":
                print(" ", end="")
            elif letter in used_letters:
                status = used_letters[letter]
                if status == 'correct':
                    print(f"{Back.GREEN}{Fore.BLACK}{letter}{Style.RESET_ALL}", end="")
                elif status == 'wrong_position':
                    print(f"{Back.YELLOW}{Fore.BLACK}{letter}{Style.RESET_ALL}", end="")
                else:  # not_in_word
                    print(f"{Back.WHITE}{Fore.BLACK}{letter}{Style.RESET_ALL}", end="")
            else:
                print(f"{letter}", end="")
        print()


def print_game_board(guesses: List[str], results: List[List[str]]):
    """
    Print the game board with all previous guesses.
    
    Args:
        guesses (List[str]): List of previous guesses
        results (List[List[str]]): List of result lists for each guess
    """
    print(f"\n{Fore.CYAN}Game Board:{Style.RESET_ALL}")
    print("  " + "-" * 25)
    
    for i in range(6):
        if i < len(guesses):
            print_guess_result(guesses[i], results[i])
        else:
            print("  " + " ___ " * 5)
    print("  " + "-" * 25)


def print_win_message(attempts: int):
    """
    Print a win message with the number of attempts.
    
    Args:
        attempts (int): Number of attempts taken
    """
    print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 CONGRATULATIONS! 🎉{Style.RESET_ALL}")
    print(f"{Fore.GREEN}You guessed the word in {attempts} {'attempt' if attempts == 1 else 'attempts'}!")
    
    # Add some fun messages based on attempts
    if attempts == 1:
        print(f"{Fore.YELLOW}Incredible! First try! 🚀{Style.RESET_ALL}")
    elif attempts == 2:
        print(f"{Fore.YELLOW}Amazing! You're a word wizard! ✨{Style.RESET_ALL}")
    elif attempts == 3:
        print(f"{Fore.YELLOW}Great job! Well played! 👏{Style.RESET_ALL}")
    elif attempts <= 5:
        print(f"{Fore.YELLOW}Good work! You got it! 👍{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Phew! That was close! 😅{Style.RESET_ALL}")


def print_lose_message(correct_word: str):
    """
    Print a lose message with the correct word.
    
    Args:
        correct_word (str): The correct word that wasn't guessed
    """
    print(f"\n{Fore.RED}{Style.BRIGHT}😔 GAME OVER! 😔{Style.RESET_ALL}")
    print(f"{Fore.RED}You ran out of attempts!")
    print(f"The correct word was: {Fore.YELLOW}{Style.BRIGHT}{correct_word.upper()}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Better luck next time! 💪{Style.RESET_ALL}")


def print_statistics(stats: dict):
    """
    Print game statistics.
    
    Args:
        stats (dict): Dictionary containing game statistics
    """
    try:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📊 GAME STATISTICS 📊{Style.RESET_ALL}")
        print("=" * 30)
        
        if 'games_played' in stats:
            print(f"Games Played: {stats['games_played']}")
        
        if 'games_won' in stats:
            win_rate = (stats['games_won'] / stats['games_played']) * 100 if stats['games_played'] > 0 else 0
            print(f"Games Won: {stats['games_won']} ({win_rate:.1f}%)")
        
        if 'current_streak' in stats:
            print(f"Current Streak: {stats['current_streak']}")
        
        if 'max_streak' in stats:
            print(f"Max Streak: {stats['max_streak']}")
        
        if 'guess_distribution' in stats:
            print(f"\n{Fore.YELLOW}Guess Distribution:{Style.RESET_ALL}")
            for i in range(1, 7):
                count = stats['guess_distribution'].get(i, 0)
                bar = "█" * count if count > 0 else "░"
                print(f"{i}: {bar} {count}")
        
        print("=" * 30)
    except Exception as e:
        print(f"⚠️  Could not display statistics: {e}")


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_user_input(prompt: str) -> str:
    """
    Get user input with a prompt.
    
    Args:
        prompt (str): The prompt to display
        
    Returns:
        str: User input
    """
    return input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL}").strip()


def validate_guess(guess: str, word_list) -> Tuple[bool, str]:
    """
    Validate a user's guess.
    
    Args:
        guess (str): The guessed word
        word_list: The word list object
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not guess:
        return False, "Please enter a word."
    
    if len(guess) != 5:
        return False, "Word must be exactly 5 letters long."
    
    if not guess.isalpha():
        return False, "Word must contain only letters."
    
    if not word_list.is_valid_word(guess):
        return False, "Word not found in the word list."
    
    return True, ""


def calculate_guess_result(guess: str, target_word: str) -> List[str]:
    """
    Calculate the result of a guess against the target word.
    
    Args:
        guess (str): The guessed word
        target_word (str): The target word
        
    Returns:
        List[str]: List of result indicators
    """
    result = ['not_in_word'] * 5
    target_letters = list(target_word)
    guess_letters = list(guess)
    
    # First pass: mark correct letters
    for i in range(5):
        if guess_letters[i] == target_letters[i]:
            result[i] = 'correct'
            target_letters[i] = None  # Mark as used
            guess_letters[i] = None   # Mark as used
    
    # Second pass: mark wrong position letters
    for i in range(5):
        if guess_letters[i] is not None:
            if guess_letters[i] in target_letters:
                result[i] = 'wrong_position'
                # Remove the first occurrence of this letter from target
                for j in range(5):
                    if target_letters[j] == guess_letters[i]:
                        target_letters[j] = None
                        break
    
    return result


def update_used_letters(guess: str, result: List[str], used_letters: dict) -> dict:
    """
    Update the used letters dictionary based on guess result.
    
    Args:
        guess (str): The guessed word
        result (List[str]): Result of the guess
        used_letters (dict): Current used letters dictionary
        
    Returns:
        dict: Updated used letters dictionary
    """
    for letter, status in zip(guess.upper(), result):
        if letter not in used_letters:
            used_letters[letter] = status
        else:
            # Upgrade status if current is better (correct > wrong_position > not_in_word)
            current_status = used_letters[letter]
            if status == 'correct' or (status == 'wrong_position' and current_status == 'not_in_word'):
                used_letters[letter] = status
    
    return used_letters 