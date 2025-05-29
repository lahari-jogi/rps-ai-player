import random
from collections import Counter

# === Define all bot opponents ===

def quincy(_):
    # Cycles through R, R, P, P, S
    quincy.cycle = getattr(quincy, 'cycle', 0)
    sequence = ['R', 'R', 'P', 'P', 'S']
    move = sequence[quincy.cycle % len(sequence)]
    quincy.cycle += 1
    return move

def abbey(prev_opponent_play):
    abbey.last_two = getattr(abbey, 'last_two', '')
    abbey.transitions = getattr(abbey, 'transitions', {})
    if prev_opponent_play:
        abbey.last_two += prev_opponent_play
        abbey.last_two = abbey.last_two[-2:]

    guess = 'R'
    if len(abbey.last_two) == 2 and abbey.last_two in abbey.transitions:
        guess = max(abbey.transitions[abbey.last_two], key=abbey.transitions[abbey.last_two].get)

    result = {'R': 'P', 'P': 'S', 'S': 'R'}[guess]

    if len(abbey.last_two) == 2:
        if abbey.last_two not in abbey.transitions:
            abbey.transitions[abbey.last_two] = {}
        abbey.transitions[abbey.last_two][prev_opponent_play] = \
            abbey.transitions[abbey.last_two].get(prev_opponent_play, 0) + 1

    return result

def kris(prev_opponent_play):
    if not prev_opponent_play:
        return "R"
    return {'R': 'P', 'P': 'S', 'S': 'R'}[prev_opponent_play]

def mrugesh(prev_opponent_play):
    mrugesh.opponent_history = getattr(mrugesh, 'opponent_history', [])
    if prev_opponent_play:
        mrugesh.opponent_history.append(prev_opponent_play)
    if len(mrugesh.opponent_history) < 10:
        guess = "R"
    else:
        last_10 = mrugesh.opponent_history[-10:]
        most_frequent = max(set(last_10), key=last_10.count)
        ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
        guess = ideal_response[most_frequent]
    return guess

# === Your player function ===

def player(prev_opponent_play):
    if not hasattr(player, "my_history"):
        player.my_history = []
        player.opponent_history = []
        player.counter_moves = {'R': 'P', 'P': 'S', 'S': 'R'}

    if prev_opponent_play:
        player.opponent_history.append(prev_opponent_play)

    round_number = len(player.my_history)

    if round_number == 0:
        move = 'R'
    else:
        # --- Kris: counters your last move
        last_my_move = player.my_history[-1]
        kris_pred = player.counter_moves[last_my_move]
        kris_counter = player.counter_moves[kris_pred]

        # --- Mrugesh: counters your most frequent move in last 10
        from collections import Counter
        recent_moves = player.my_history[-10:] if round_number >= 10 else player.my_history
        if recent_moves:
            most_common_my = Counter(recent_moves).most_common(1)[0][0]
        else:
            most_common_my = 'R'
        mrugesh_pred = player.counter_moves[most_common_my]
        mrugesh_counter = player.counter_moves[mrugesh_pred]

        # --- Abbey: uses transition matrix to predict next move
        if round_number >= 2:
            last_two = player.opponent_history[-2:]
            transition_counts = {}
            for i in range(len(player.opponent_history) - 2):
                key = (player.opponent_history[i], player.opponent_history[i+1])
                next_move = player.opponent_history[i+2]
                if key not in transition_counts:
                    transition_counts[key] = Counter()
                transition_counts[key][next_move] += 1
            key = tuple(last_two)
            if key in transition_counts:
                abbey_pred = transition_counts[key].most_common(1)[0][0]
            else:
                abbey_pred = player.opponent_history[-1]
        else:
            abbey_pred = 'R'
        abbey_counter = player.counter_moves[abbey_pred]

        # --- Quincy: fixed 5-move cycle: R, R, P, P, S
        quincy_cycle = ['R', 'R', 'P', 'P', 'S']
        predicted_quincy = quincy_cycle[round_number % 5]
        quincy_counter = player.counter_moves[predicted_quincy]

        # --- Final move: majority vote among predicted counters
        move_options = [kris_counter, mrugesh_counter, abbey_counter, quincy_counter]
        move = Counter(move_options).most_common(1)[0][0]

    player.my_history.append(move)
    return move


# === Play function ===

def play(player1, player2, num_games=1000, verbose=False):
    p1_prev = ""
    p2_prev = ""
    results = {"p1": 0, "p2": 0, "tie": 0}
    for _ in range(num_games):
        p1_play = player1(p2_prev)
        p2_play = player2(p1_prev)

        if verbose:
            print(f"Player 1: {p1_play}  Player 2: {p2_play}")

        if p1_play == p2_play:
            results["tie"] += 1
        elif beats(p1_play, p2_play):
            results["p1"] += 1
        else:
            results["p2"] += 1

        p1_prev = p1_play
        p2_prev = p2_play

    print("Final results:", results)
    win_rate = results["p1"] / num_games * 100
    print(f"Player 1 win rate: {win_rate}%")
    return win_rate

def beats(one, two):
    return (one == 'R' and two == 'S') or \
           (one == 'S' and two == 'P') or \
           (one == 'P' and two == 'R')

# === Test against all bots ===

if __name__ == "__main__":
    bots = [quincy, abbey, kris, mrugesh]
    for bot in bots:
        print(f"Testing game against {bot.__name__}...")
        win_rate = play(player, bot, 1000, verbose=False)
        if win_rate > 60:
            print(f"Pass! Player wins against {bot.__name__} with {win_rate:.2f}% win rate.\n")
        else:
            print(f"Fail! Player loses against {bot.__name__} with only {win_rate:.2f}% win rate.\n")