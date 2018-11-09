import string, re, itertools
import timed_call

def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(re.findall(r'[A-Z]',formula)) #should be a string
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield formula.translate(table)

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
    
print(valid("2 + 202 == 204"))
print(valid("02 + 2 == 4"))
print(valid("2 + 02 == 4"))
print(valid("2 + 2 == 04"))
print(valid("2 / 0 == 4"))

print(solve('ODD + ODD == EVEN'))