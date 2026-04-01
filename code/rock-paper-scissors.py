"""
Project: Rock Paper Scissors

Starting point extracted from the companion book.
This code is intentionally incomplete — the book walks
you through building the full version step by step.
Complete it as an exercise using the skills and
techniques from the chapter.
"""

# Test every combination manually first
def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        return "player"
    else:
        return "computer"
