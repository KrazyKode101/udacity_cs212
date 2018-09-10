import sys
from enum import Enum

class HandCategory(Enum):
    FIVE_OF_A_KIND = 9
    STRAIGHT_FLUSH = 8
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 6
    FLUSH = 5
    STRAIGHT = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_HAND = 0
    INVALID = -1

def find_hand_category(hand):
    "Return the hand_rank category of hand"
    #todo
    return HandCategory.FIVE_OF_A_KIND

def compare(hand1,hand2):
    "Return highest hand between hand1 and hand2"
    #todo
    return True

class HandWrapper:
    "class encapsulating 'list representation of hand'"

    def __init__(self,hand):
        self.hand = hand
        self.category = find_hand_category(hand)

    def __lt__(self,handWrapper):
        if self.category < handWrapper.category:
            return True
        else:
            compare(self.hand,handWrapper.hand)

def poker(hands):
    "Return the best hand : poker([hand,...]) => hand"

    hand_objs = [HandWrapper(e) for e in hands]
    winner = max(hand_objs)

    return winner.hand

hands = [ [('9','C'), ('9','S'), ('9','H'), ('9','D'), ('J','None')] ]

print(poker(hands))