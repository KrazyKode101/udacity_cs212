"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""
import collections

def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    # your code here (I won't repeat "your code here"; there's one for each function)

    if not isinstance(coefs, tuple) or len(coefs)==0:
        return None

    def compute_poly(x):
        result = 0
        power = 0
        for e in compute_poly.coefs:
            result += (e * x**power)
            power += 1
        return result

    compute_poly.coefs = coefs
    poly_name = ""

    power = len(coefs) - 1
    is_first_term = True
    for e in reversed(coefs):
        if e == 0:
            continue

        if not is_first_term:
            poly_name += " "

        if e <= -1:
            poly_name += "- "
        elif e >= 1 and not is_first_term:
            poly_name += "+ "

        if e == -1 or e == 1:
            if power == 0:
                poly_name += "1"
            elif power == 1:
                poly_name += 'x'
            else:
                poly_name += ("x**" + str(power))
        else:
            poly_name += str(e)
            if power == 1:
                poly_name += " * x"
            elif power > 1:
                poly_name += (" * x**" + str(power))

        is_first_term = False
        power -= 1

    compute_poly.__name__ = poly_name
    return compute_poly

def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 =  add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27) 
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573

def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)

def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return hasattr(x,"coefs")

def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    l1 = p1.coefs
    l2 = p2.coefs
    diff_len = abs(len(l1)-len(l2))

    if len(l1) > len(l2):
        l2 = l2 + tuple([0]*diff_len)
    else:
        l1 = l1 + tuple([0]*diff_len)

    return poly(tuple(map(lambda x,y:x+y,l1,l2)))

def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    l1 = p1.coefs
    l2 = p2.coefs
    diff_len = abs(len(l1)-len(l2))

    if len(l1) > len(l2):
        l2 = l2 + tuple([0]*diff_len)
    else:
        l1 = l1 + tuple([0]*diff_len)

    return poly(tuple(map(lambda x,y:x-y,l1,l2)))

def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    n1 = len(p1.coefs)
    n2 = len(p2.coefs)
    n_result = (n1-1) + (n2-1) + 1
    result = [0]*n_result

    for (i,e1) in enumerate(p1.coefs):
        for (j,e2) in enumerate(p2.coefs):
            result[i+j] += (e1*e2)
    
    return poly(tuple(result))

def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    if n == 0:
        return poly((1))
    else:
        result = p
        for i in range(1,n):
            result = mul(result,p)
        return result

"""
If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""
    
def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    deriv_coefs = ( i*coef for (i,coef) in enumerate(p.coefs) if i > 0 )
    return poly(tuple(deriv_coefs))

def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    integral_coefs = ( coef//i for (i,coef) in enumerate(p.coefs,1) )
    integral_coefs = (C,) + tuple(integral_coefs)
    return poly(integral_coefs)

"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""

def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
    assert p1(100) == newp1(100) # The new poly objects are still callable.
    assert same_name(p1.__name__,newp1.__name__)
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))

def Poly(str_poly):
    func = eval("lambda x: {}".format(str_poly))
    func.__name__ = str_poly
    return func

def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert same_name(p1.__name__,newp1.__name__)

test_poly()
test_poly2()