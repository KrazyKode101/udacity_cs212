import os,sys
import itertools,math
sys.path.append(r"C:\Users\kartts\Google Drive\GoogleDrive\computer science\projectcodes\miscellaneous_scripts")
from debug_utils import trace

@trace
def solve_bridge_puzzle(people_at_left,people_at_right=(),cur_torch_pos='l',computed_timings={},consumed_time=0):

    if len(people_at_left) == 0 and cur_torch_pos == 'r':
        return consumed_time

    if (people_at_left,people_at_right,cur_torch_pos) in computed_timings:
        return computed_timings[(people_at_left,people_at_right,cur_torch_pos)]

    min_crossing_time = math.inf
    if cur_torch_pos == 'l':
        for people_crossing_bridge in itertools.combinations(people_at_left,2):
            updated_people_at_left = tuple(filter(lambda x : x not in people_crossing_bridge, people_at_left))
            updated_people_at_right = people_at_right + tuple(people_crossing_bridge)
            updated_crossing_time = consumed_time + max(people_crossing_bridge)
            min_crossing_time = min(min_crossing_time, solve_bridge_puzzle(updated_people_at_left,updated_people_at_right,'r',computed_timings,updated_crossing_time))
    elif cur_torch_pos == 'r':
        for people_crossing_bridge in itertools.combinations(people_at_right,1):
            updated_people_at_right = tuple(filter(lambda x : x not in people_crossing_bridge, people_at_right))
            updated_people_at_left = people_at_left + tuple(people_crossing_bridge)
            updated_crossing_time = consumed_time + max(people_crossing_bridge)
            min_crossing_time = min(min_crossing_time, solve_bridge_puzzle(updated_people_at_left,updated_people_at_right,'l',computed_timings,updated_crossing_time))

    computed_timings[(people_at_left,people_at_right,cur_torch_pos)] = min_crossing_time
    return min_crossing_time

def test():
    print(solve_bridge_puzzle((1,2,5,10)))

if __name__ == "__main__":
    test()