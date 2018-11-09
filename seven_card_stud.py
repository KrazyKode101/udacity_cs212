import itertools
import poker

black_cards = [ rank+suit for rank in "23456789TJQKA" for suit in "SC"  ]
red_cards = [ rank+suit for rank in "23456789TJQKA" for suit in "DH"  ]

def best_hand(hand):
    "From a 7-card hand, return the best 5 card hand."
    
    return max(itertools.combinations(hand,5),key=poker.hand_rank)

def test_best_hand():
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_hand passes'

print(test_best_hand())

def replacement(card):
    if card == "?B": return black_cards
    elif card == "?R" : return red_cards
    else: return [card]

def best_wild_hand_v3(hand):
    hands = set(best_hand(h) for h in itertools.product(*map(replacement,hand)))
    return max(hands,key=poker.hand_rank)

def enumerate_hands(comb):
    try:
        bj_pos = comb.index("?B")
    except:
        bj_pos = -1
    
    try:
        rj_pos = comb.index("?R")
    except:
        rj_pos = -1

    if bj_pos != -1 and rj_pos!=-1:
        for b in black_cards:
            if b not in comb:
                for r in red_cards:
                    if r not in comb:
                        l = comb.copy()
                        l[bj_pos] = b
                        l[rj_pos] = r
                        yield l

    elif rj_pos != -1:
        for e in red_cards:
            if e not in comb:
                l = comb.copy()
                l[rj_pos] = e
                yield l

    elif bj_pos != -1:
        for e in black_cards:
            if e not in comb:
                l = comb.copy()
                l[bj_pos] = e
                yield l
    
    else:
        yield comb

def best_wild_hand_v2(hand):
    five_card_combs = itertools.combinations(hand,5)
    result = [] 
    for comb in five_card_combs:
        comb = list(comb)
        combs = enumerate_hands(comb)
        max_of_combs = max(combs,key=poker.hand_rank)
        result.append(max_of_combs)

    return max(result,key=poker.hand_rank)

def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    
    five_card_combs = itertools.combinations(hand,5)
    result = []
    for comb in five_card_combs:
        comb = list(comb)
        try:
            bj_pos = comb.index("?B")
        except:
            bj_pos = -1
        
        try:
            rj_pos = comb.index("?R")
        except:
            rj_pos = -1

        temp = []

        if bj_pos != -1 and rj_pos!=-1:
            for b in black_cards:
                if b not in comb:
                    for r in red_cards:
                        if r not in comb:
                            l = comb.copy()
                            l[bj_pos] = b
                            l[rj_pos] = r
                            temp.append(l)

        elif rj_pos != -1:
            for e in red_cards:
                if e not in comb:
                    l = comb.copy()
                    l[rj_pos] = e
                    temp.append(l)

        elif bj_pos != -1:
            for e in black_cards:
                if e not in comb:
                    l = comb.copy()
                    l[bj_pos] = e
                    temp.append(l)
        
        else:
            temp = [comb]

        result.append(max(temp,key=poker.hand_rank))

    return max(result,key=poker.hand_rank)

def test_best_wild_hand():
    assert (sorted(best_wild_hand_v3("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand_v3("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand_v3("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    return 'test_best_wild_hand passes'

print(test_best_wild_hand())