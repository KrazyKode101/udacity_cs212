from collections import defaultdict
import random

mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

hand_names = {
    0 : "high card",
    1 : "2 of a kind",
    2 : "2-pair",
    3 : "3 of a kind",
    4 : "straight",
    5 : "flush",
    6 : "full house",
    7 : "four of a kind",
    8 : "straight flush",
}

def swap(deck,i,j):
    deck[i], deck[j] = deck[j], deck[i]

def shuffle(deck):
    n = len(deck)
    for i in range(n-1):
        swap(deck,i,random.randint(i,n-1))

def deal(numhands, n=5, deck=mydeck):
    "deal out 'numhands' hands of 'n' cards each after shuffling"
    #run python's shuffle algo
    #random.shuffle(mydeck)
    
    #run custom shuffling algo
    shuffle(deck) 

    #prepare hands of 'n' cards each
    return [deck[n*i:n*(i+1)] for i in range(0,numhands)]

def factorial(n):
    if(n<=0):
        return 1
    else:
        return factorial(n-1) * n

def test_shuffler(shuffler, deck, num_iter):
    "Tests if the shuffler shuffles good"
    counts = defaultdict(int)
    for _ in range(num_iter):
        input = list(deck)
        shuffle(input)
        counts[''.join(input)] += 1
    
    expected_count = num_iter * (1/factorial(len(deck)))

    isShufflerGood = all( (0.9 <= counts[e]/expected_count <= 1.1) for e in counts )

    name = shuffler.__name__

    print("%s(%s) %s" % (name,deck,"good" if isShufflerGood else "bad"))

    for key,value in counts.items():
        print("%s: attained=>%7.4f%% expected=>%7.4f%%" % (key, (value/num_iter)*100, (expected_count/num_iter)*100))

    return isShufflerGood

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    assert(ranks)
    
    return (max(ranks)-min(ranks)==4 and len(set(ranks))==5)

def flush(hand):
    "Return True if all the cards have the same suit."
    assert(hand)
    
    suits = [s for r,s in hand]
    return (len(set(suits))==1)

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    assert(ranks)
    
    counts = defaultdict(int)
    for e in ranks:
        counts[e] += 1
    
    for k,v in counts.items():
        if v == n:
            return k
    
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    assert(ranks)

    temp = set(ranks)
    if len(temp) != 3:
        return None
    
    h = None
    l = None
    for e in temp:
        if ranks.count(e) == 2:
            if h==None:
                h = e
            else:
                l = e
    
    if h==None and l==None:
        return None
    else:
        return (h,l)

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."

    ranks = ['--23456789TJQKA'.index(r[0]) for r in cards]
    ranks.sort(reverse=True)

    #to handle: ace can rank either above K or below 2
    if(ranks == [14,5,4,3,2]):
        ranks = [5,4,3,2,1]

    return ranks

def hand_rank(hand):
    "Returns the rank of the hand in the form of a tuple"
    
    ranks = card_ranks(hand)
    
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6, kind(3,ranks), kind(2,ranks))
    elif flush(hand):                              # flush
        return (5, ranks)
    elif straight(ranks):                          # straight  
        return (4, max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3, kind(3,ranks), ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):                           # kind
        return (1, kind(2,ranks), ranks)
    else:                                          # high card
        return (0,ranks)

def hand_percentages(n=700*1000):
    "Prints a table indicating probablity of each type of hand"
    counts = [0]*9
    for i in range(int(n/10)):
        for hand in deal(10):
            rank = hand_rank(hand)[0]
            counts[rank] += 1
    
    for i in reversed(range(9)):
        print("%14s : %7.4f%%" % (hand_names[i],100*counts[i]/n))

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."

    result, maxval = [],None
    key = key or (lambda x : x)

    for x in iterable:
        xval = key(x)
        if not result or xval > maxval:
            result, maxval = [x], xval
        elif xval == maxval:
            result.append(x)

    return result

def poker(hands):
    "Return the best hand: poker([hand,...]) => hand"
    if not hands:
        return False

    return allmax(hands, key=hand_rank)

def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    st1 = "AC 2S 3H 4D 5H".split() # Straight
    st2 = "AS 2C 3D 4D 5H".split() # Straight

    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([st1,st2]) == [st1,st2]

    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    
    assert straight([9, 8, 7, 6, 5]) == True
    assert straight([9, 8, 8, 6, 5]) == False
    
    assert flush(sf) == True
    assert flush(fk) == False

    assert card_ranks(st1) == [5,4,3,2,1]
    assert card_ranks(st2) == [5,4,3,2,1]

    print(deal(4))

    hand_percentages(4000)

    test_shuffler(shuffle,"abcd",10000)

    return 'tests pass'

test()