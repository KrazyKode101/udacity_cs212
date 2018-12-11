# --------------
# User Instructions
#
# Complete the code for the compiler by completing the constructor
# for the patterns alt(x, y) and oneof(chars). 

def genseq_v1(x,y,Ns):
    Nss = range(max(Ns)+1)
    return set(m1+m2
                for m1 in x(Nss) for m2 in y(Nss)
                if len(m1+m2) in Ns)

def genseq(x,y,Ns,minlenx=0):
    if not Ns:
        return null

    x_matches = x(range(minlenx,max(Ns)+1))
    x_Ns = set(len(each) for each in x_matches)
    y_matches = y(set(n-m for m in x_Ns for n in Ns if n-m>=0))

    return set(m1+m2
               for m1 in x_matches
               for m2 in y_matches 
               if len(m1+m2) in Ns)

def lit(s):         return lambda Ns: set([s]) if len(s) in Ns else null
def lit_v2(s):
    set_s = set([s])
    return lambda Ns: set_s if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, minlenx=1)
def oneof(chars):   return lambda Ns: set(chars) if 1 in Ns else null
def oneof_v2(chars):
    set_chars = set(chars)
    return lambda Ns: set_chars if 1 in Ns else null
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.

null = frozenset([])

def test():
    
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null 
    
    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])
    
    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null

    k = seq(seq(lit('hi'),lit('bye')),seq(lit('hello'),lit('howru')))
    print(k(set([1,2,3,5,10,12,15])))

    return 'tests pass'

print(test())