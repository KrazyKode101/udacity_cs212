import os,sys

def can_apply_action(e,cap,vol):
    if e[0] == "empty":
        return cap[e[1]]!=0
    elif e[0] == "full":
        return cap[e[1]]!=vol[e[1]]
    elif e[0] == "pour":
        return cap[e[1]]!=0 and cap[e[2]]!=vol[e[2]]
    else:
        assert False,"unknown action"

def apply_action(e,cap,vol):
    cap = list(cap)
    if e[0] == "empty":
        cap[e[1]] = 0
    elif e[0] == "full":
        cap[e[1]] = vol[e[1]]
    elif e[0] == "pour":
        max_deficit = vol[e[2]] - cap[e[2]]
        if cap[e[1]] >= max_deficit:
           cap[e[2]] = vol[e[2]]
           cap[e[1]] -= max_deficit
        else:
            cap[e[2]] += cap[e[1]]
            cap[e[1]] = 0
    else:
        assert False,"unknown action"
    return tuple(cap)

def find_measurement_util(cur_cap,vol,goal,actions,visited,onstack):
    if cur_cap not in visited:
        visited[cur_cap] = True
        onstack.append(cur_cap)
    else:
        return False
    
    for e in actions:
        if can_apply_action(e,cur_cap,vol):
            new_cap = apply_action(e,cur_cap,vol)
            if goal in new_cap:
                onstack.append(new_cap)
                return True
            elif find_measurement_util(new_cap,vol,goal,actions,visited,onstack):
                return True

    onstack.pop()
    return False

def find_measurement(vol,goal):
    actions = [('empty',0),('empty',1),('full',0),('full',1),('pour',0,1),('pour',1,0)]
    visited = {}
    onstack = []
    start_cap = (0,0)

    isTargetFound = find_measurement_util(start_cap,vol,goal,actions,visited,onstack)
    print(isTargetFound,onstack)

find_measurement((9,4),6)
find_measurement((9,4),5)
find_measurement((9,4),50)