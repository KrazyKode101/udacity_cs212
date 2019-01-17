import re

def trace(f):
    indent = '   '
    level = 0
    def _f(*args):
        nonlocal level
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print('%s--> %s' % (level*indent, signature))
        level += 1
        try:
            result = f(*args)
        finally:
            level -= 1
        print('%s<-- %s == %s' % ((level)*indent, signature, result))
        return result
    return _f

def split(text,sep=" "):
    return [t.strip() for t in text.strip().split(sep) if t]

def get_grammar(descr,whitespace="\s*"):
    result = {}
    result[" "] = whitespace
    for rule in split(descr,"\n"):
        key,value = split(rule,"=>")
        alternatives = split(value,"|")
        result[key] =  tuple(map(split,alternatives))
    return result

Fail = (None,None)

def parse(start_nonterminal,grammar,text):
    regex = grammar[" "] + "(%s)"

    def parse_sequence(sequence,text):
        tree = [] 
        for atom in sequence:
            t, rem = parse_atom(atom,text)
            if rem is not None:
                text = rem
                if t:
                    tree.append(t) 
            else:
                return Fail 

        return (tree,text)

    def parse_atom(atom,text):
        if atom in grammar:
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative,text)
                if rem is not None:
                    if tree:
                        return [atom] + tree, rem
                    else:
                        return [],rem
            return Fail
        else:
            if "Empty" == atom:
                return [],text
            else:
                m = re.match(regex % atom,text)
                if m != None:
                    return m.group(1), text[m.end():]
                else:
                    return Fail

    return parse_atom(start_nonterminal,text)

JSON = get_grammar("""
json => value
value => object | array | string | number | true | false | null
object => \{ members } | \{ ws \}
members => member , members | member
member => ws string ws : element
array => \[ elements \] | \[ ws \]
elements => element , elements | element
element => ws value ws
string => "[^"]*"
hex => digit | [A-F] | [a-f]
number => int frac exp
int => [+-]? digits
digits => digit digits | digit
digit => \d
frac => . digits | Empty
exp => [Ee]? [+-]? digits | Empty
ws => 0009 ws | 000a ws | 000d ws | 0020 ws | Empty
""")

def json_parse(text):
    return parse('value', JSON, text)

def test():
    print(json_parse('["testing", 1, 2, 3]'),end="\n\n")
    print(json_parse('-123.456e+789'),end="\n\n")
    print(json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}'),end="\n\n")
    return("tests pass")

test()