# -----------------
# User Instructions
# 
# Write a function, csuccessors, that takes a state (as defined below) 
# as input and returns a dictionary of {state:action} pairs. 
#
# A state is a tuple with six entries: (M1, C1, B1, M2, C2, B2), where 
# M1 means 'number of missionaries on the left side.'
#
# An action is one of the following ten strings: 
#
# 'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C', '<-CC'
# where 'MM->' means two missionaries travel to the right side.
# 
# We should generate successor states that include more cannibals than
# missionaries, but such a state should generate no successors.

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    result = {}
    
    if (M1 != 0 and C1 > M1) or (M2 != 0 and C2 > M2):
        return result
    
    to_remove = ((1,0),(0,1),(2,0),(0,2),(1,1))
    
    for each in to_remove:
        if B1 == 1:
            new_successor = M1-each[0],C1-each[1],0,M2+each[0],C2+each[1],1
            action = "M"*each[0] + "C"*each[1] + "->"
        elif B2 == 1:
            new_successor = M1+each[0],C1+each[1],1,M2-each[0],C2-each[1],0
            action = "<-" + "M"*each[0] + "C"*each[1]
        else:
            assert False,"invalid number of boats: B1={} and B2={}".format(B1,B2)
            
        negative_check = all(e>=0 for e in new_successor)
        
        if negative_check:
            result[new_successor] = action
    
    return result

def is_safe_state(state):
    M1, C1, _, M2, C2, _ = state
    return (M1==0 or C1<=M1) and (M2==0 or C2<=M2)

def mc_problem(start,goal,path,visited={}):
    if start == goal:
        return True
    
    visited[start] = True
    successors = csuccessors(start)
    for successor,action in successors.items():
        if is_safe_state(successor) and successor not in visited:
            path.append(action)
            path_found = mc_problem(successor,goal,path,visited)
            if path_found:
                return True
            else:
                path.pop()

    return False

def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->', 
                                               (1, 1, 0, 1, 1, 1): 'MC->', 
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M', 
                                               (3, 1, 1, 2, 3, 0): '<-MM', 
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    
    path = []
    start = (3,3,1,0,0,0)
    goal = (0,0,0,3,3,1)
    print(mc_problem(start,goal,path))
    print(path)

    return 'tests pass'

print(test())