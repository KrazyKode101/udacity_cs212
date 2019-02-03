import math

million = 1000000

def Q(state,action,U):
    if action == "hold":
        return U(state+1*million)
    elif action == "gamble":
        return U(state+3*million)*0.5 + U(state)*0.5
    else:
        raise KeyError

def actions(state) : return ['hold','gamble']

def identiy(x) : return x

def best_action(state,actions,Q,U):
    def EU(action) : return Q(state,action,U)
    return max(actions(state), key=EU)

print(best_action(100,actions,Q,identiy))
print(best_action(1*million,actions,Q,identiy))
print(best_action(10*million,actions,Q,identiy))

print(best_action(100,actions,Q,math.log))
print(best_action(1*million,actions,Q,math.log))
print(best_action(10*million,actions,Q,identiy))
