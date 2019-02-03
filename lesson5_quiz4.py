# -----------------
# User Instructions
# 
# Write a function, play_pig, that takes two strategy functions as input,
# plays a game of pig between the two strategies, and returns the winning
# strategy. Enter your code at line 41.
#
# You may want to borrow from the random module to help generate die rolls.

import random

possible_moves = ['roll', 'hold']
other = {1:0, 0:1}
goal = 50

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

def hold_at(x):
    """Return a strategy that holds if and only if 
    pending >= x or player reaches goal."""
    def strategy(state):
        # your code here
        _, me, _, pending = state
        return "roll" if (me+pending < goal) and pending < x else "hold"
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    (p, me, you, pending) = state
    return (other[p], you, me+pending, 0)

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    (p, me, you, pending) = state
    if d == 1:
        return (other[p], you, me+1, 0) # pig out; other player's turn
    else:
        return (p, me, you, pending+d)  # accumulate die roll in pending

def roll_die():
    return random.randint(1,6)

def play_pig(A, B):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    # your code here
    players = [A,B]
    cur_player = random.randint(0,len(players)-1)
    cur_state = (cur_player,0,0,0)

    while True:
        cur_player,cur_player_score,other_player_score,_ = cur_state
        print("cur_state: ",cur_state)

        if cur_player_score >= goal:
            return players[cur_player]
        elif other_player_score >= goal:
            return players[other[cur_player]]
        
        next_move = players[cur_player](cur_state)

        if next_move == "hold":
            print("player {} holded".format(cur_player))
            cur_state = hold(cur_state)
        elif next_move == "roll":
            die_val = roll_die()
            print("player {} rolled {}".format(cur_player,die_val))
            cur_state = roll(cur_state,die_val)
    
    return None

def always_roll(state):
    _,cur_player_score,_,pending = state
    if cur_player_score + pending >= 50:
        return 'hold'
    else:
        return 'roll'

def always_hold(state):
    return 'hold'

def test():
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll' #why always roll wins here
    return 'tests pass'

print(test())