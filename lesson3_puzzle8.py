import re

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
            if (t,rem) != Fail:
                text = rem
                tree.append(t) 
            else:
                return Fail 

        return (tree,text)

    def parse_atom(atom,text):
        if atom == "Empty":
            return ([],text)
        elif atom in grammar:
            for alternative in grammar[atom]:
                (tree, rem) = parse_sequence(alternative,text)
                if (tree,rem) != Fail:
                    return [atom] + tree, rem
            return Fail
        else:
            m = re.match(regex % atom,text)
            if m != None:
                return ( m.group(1), text[m.end():] )
            else:
                return Fail

    return parse_atom(start_nonterminal,text)

grammar = r"""
Exp     => Term [+-] Exp | Term
Term    => Factor [*/] Term | Factor
Factor  => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps    => Exp [,] Exps | Exp | Empty
Var     => [a-zA-Z_]\w*
Num     => [-+]?[0-9]+([.][0-9]*)?
"""

G = get_grammar(grammar)
text = "(m* x + b) - 1 + f(a) /10"

def test():
    tree,rem = parse("Exp",G,text)
    print("tree:",tree,end="\n\n")
    print("rem:",rem,end="\n\n")
    assert (tree,rem)!=Fail
    assert len(rem)==0
    print("test passes")

test()