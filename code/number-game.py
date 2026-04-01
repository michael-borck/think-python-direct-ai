"""
Project: Number Guessing Game

Starting point extracted from the companion book.
This code is intentionally incomplete — the book walks
you through building the full version step by step.
Complete it as an exercise using the skills and
techniques from the chapter.
"""

# Problem: Crashes on non-numeric input
guess = int(input("Guess: "))  # Crashes on "hello"

# Solution: Handle gracefully
try:
    guess = int(input("Guess: "))
except ValueError:
    print("Please enter a number!")
    continue
