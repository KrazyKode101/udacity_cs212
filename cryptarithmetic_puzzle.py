import string, re, itertools

import re

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""

    if word.isupper():
        terms = [ ('%s*%s' % (10**i,ch)) for i,ch in enumerate(word[::-1]) ]
        return "(" + '+'.join(terms) + ")"
    else:
        return word

def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall(r'[A-Z]',formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield str.translate(formula,table)

def valid(f):
    "Formula f is valid iff it has no numbers with leading zero and evals true."
    try:
        return (not re.search(r'\b0\d+',f)) and (eval(f) == True)
    except ArithmeticError:
        return False

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f

def compile_formula(formula):
    """compile formula into a function. Also, return letters found in formula as a str
    in the same order as params of the function"""
    letters = ''.join(set(re.findall(r'[A-Z]',formula)))
    params = ' , '.join(letters)
    body = ''.join(map(compile_word,re.split(r'([A-Z]+)',formula)))
    func = "lambda %s : %s" % (params,body)
    return eval(func),letters

def compile_formula_v2(formula,verbose=False):
    """compile formula into a function. Also, return letters found in formula as a str
    in the same order as params of the function"""
    letters = ''.join(set(re.findall(r'[A-Z]',formula)))
    params = ' , '.join(letters)
    body = ''.join(map(compile_word,re.split(r'([A-Z]+)',formula)))
    leading_letters = set(re.findall(r'([A-Z])[A-Z]*',formula))
    if leading_letters:
        leading_zero_check = ' and '.join(e+'!=0' for e in leading_letters)
        body = "%s and (%s)" % (leading_zero_check,body) 
    func = "lambda %s : (%s)" % (params,body)
    if verbose: print(func)
    return eval(func),letters

def solve_v2(formula):
    "faster version of 'solve', avoids repeated calls to eval"

    eval_func,letters = compile_formula_v2(formula,False)

    for digits in itertools.permutations(range(0,10),len(letters)):
        try:
            if eval_func(*digits):
                table = str.maketrans(letters,''.join(map(str,digits)))
                return str.translate(formula,table)
        except ArithmeticError:
            return None

def test():
    assert(valid("2 + 202 == 204") == True)
    assert(valid("02 + 2 == 4") == False)
    assert(valid("2 + 02 == 4") == False)
    assert(valid("2 + 2 == 04") == False)
    assert(valid("2 / 0 == 4") == False)

    print(solve('ODD + ODD == EVEN'))

    print(compile_word("YOU"))

    print(compile_formula("ODD + ODD == EVEN"))
    print(compile_formula("YOU == ME**2"))

    print(solve_v2("ODD + ODD == EVEN"))
    print(solve_v2("YOU == ME**2"))
    print(solve_v2("A + B == BA"))
    print(solve_v2("X / X == X"))

    print(solve_v2("1 + 1 == 2"))

    print("all test cases passed!")

    return

test()