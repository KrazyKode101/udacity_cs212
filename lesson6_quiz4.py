import functools
from lesson6_quiz3 import word_plays

POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)

def word_score(word):
    "The sum of the individual letter point scores for this word."
    #return functools.reduce(lambda x,y: x+y, map(lambda char: POINTS[char],word))
    return sum(POINTS[char] for char in word)

def topn(hand, board_letters, n=10):
    "Return a list of the top n words that hand can play, sorted by word score."
    words = word_plays(hand, board_letters)
    return sorted(words, reverse=True, key=word_score)[:n]