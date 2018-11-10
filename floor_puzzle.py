#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def are_adjacent(floor1,floor2):
    return abs(floor1-floor2)==1

def floor_puzzle():
    bottom,_,_,_,top = [1,2,3,4,5]
    orderings = itertools.permutations(range(1,6))

    for e in orderings:
        (Hopper, Kay, Liskov, Perlis, Ritchie) = e
        if (Hopper!=top 
            and Kay!=bottom 
            and (Liskov!=top 
            and Liskov!=bottom)
            and Perlis>Kay 
            and not are_adjacent(Ritchie,Liskov) 
            and not are_adjacent(Liskov,Kay)):
            return e 
    
    return None

print(floor_puzzle())