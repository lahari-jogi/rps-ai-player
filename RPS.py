

import random

# Global variables to remember state across rounds
opponent_history = []
guess_history = []
patterns = {}

def player(prev_play, opponent_name=""):
    global opponent_history, guess_history, patterns

    if prev_play:
        opponent_history.append(prev_play)

    # Return "R" by default for first turn
    if len(opponent_history) < 5:
        return "R"

    # Use the last 4-move pattern from opponent to predict next move
    last_five = "".join(opponent_history[-5:])
    possible_moves = ["R", "P", "S"]

    if last_five not in patterns:
        patterns[last_five] = {"R": 0, "P": 0, "S": 0}

    # Update the pattern dictionary with opponent's next move
    if len(opponent_history) > 5:
        prev_pattern = "".join(opponent_history[-6:-1])
        next_move = opponent_history[-1]
        if prev_pattern not in patterns:
            patterns[prev_pattern] = {"R": 0, "P": 0, "S": 0}
        patterns[prev_pattern][next_move] += 1

    # Predict opponent's next move
    predicted_move = max(patterns[last_five], key=patterns[last_five].get)

    # Counter the predicted move
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    return counter_moves[predicted_move]
