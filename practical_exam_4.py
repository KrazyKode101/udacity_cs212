"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | | 
| G G . . . Y |
| P . . B . Y |
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

import itertools

N = 8

def get_goal_func(N):

    def is_goal(state):
        car_locs = dict(state)
        goal_loc = car_locs['@'][0]
        target_car_cur_loc = car_locs['*']
        return goal_loc in target_car_cur_loc

    return is_goal

def is_loc_occupied(state, loc):
    for e in state:
        if e[0] != '@' and loc in e[1]:
            return True
    return False

def find_possible_actions(car_name, car_locs, dir, state, N):
    actions = []
    start_loc, end_loc = car_locs[0], car_locs[-1]

    if dir == 'r':
        x = end_loc
        incr = 1
    elif dir == 'l':
        x = start_loc
        incr = -1
    elif dir == 't':
        x = start_loc
        incr = -N
    elif dir == 'd':
        x = end_loc
        incr = N
    else:
        assert False,"invalid dir"

    i = incr
    while not is_loc_occupied(state, x + i):
        actions.append((car_name,i))
        i += incr
    
    return actions

def get_possible_actions(state,N):
    possible_actions = []

    for car in state:
        car_name = car[0]
        car_locs = car[1]
        if car_name != '|' and car_name != '@':
            is_horizontally_parked = (car_locs[1] - car_locs[0]) == 1
            if is_horizontally_parked:
                possible_actions += find_possible_actions(car_name, car_locs, 'r', state, N)
                possible_actions += find_possible_actions(car_name, car_locs, 'l', state, N)
            else:
                possible_actions += find_possible_actions(car_name, car_locs, 't', state, N)
                possible_actions += find_possible_actions(car_name, car_locs, 'd', state, N)

    return possible_actions

def apply_action(state,action):
    for e in state:
        if e[0] == action[0]:
            old_car_locs = e[1]

    if old_car_locs:
        filtered_state = list(filter(lambda x: x[0]!=action[0], state))
        new_car_locs = tuple(map(lambda x: x+action[1], old_car_locs))
        filtered_state.append((action[0], new_car_locs))
        return tuple(filtered_state)
    
    return state

def get_successors_func(N):

    def successors(state):
        result = {}
        possible_actions = get_possible_actions(state,N)
        for action in possible_actions:
            new_state = apply_action(state,action)
            result[new_state] = action
        return result

    return successors

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return path_actions(shortest_path_search(start,get_successors_func(N),get_goal_func(N)))
    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple( start+(incr*i) for i in range(n) )

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    goal = (N*N)//2-1
    walls = locs(0,N) + locs(N, N-2, N) + locs(2*N-1, N-2, N) + locs((N-1)*N, N)
    walls = tuple( (e for e in walls if e != goal) )
    cars = cars + ( ('|', walls) , ('@', (goal,)) )
    return cars

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print(s,end='')
        if i % N == N - 1: print()

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set([start]) # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

print(solve_parking_puzzle(puzzle1))
print(solve_parking_puzzle(puzzle2))
print(solve_parking_puzzle(puzzle3))