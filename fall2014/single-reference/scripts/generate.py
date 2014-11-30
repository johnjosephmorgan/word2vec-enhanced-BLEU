from nltk.grammar import Nonterminal, parse_cfg 

def generate(grammar, start=None):
    if not start:
        start = grammar.start()
    return _generate_all(grammar, [start])[0]

def _generate_all(grammar, items):
    frags = []
    if len(items) == 1:
        if isinstance(items[0], Nonterminal):
            for prod in grammar.productions(lhs=items[0]):
                frags.append(_generate_all(grammar, prod.rhs()))
        else:
            frags.append(items[0])
    else:
        for frag1 in _generate_all(grammar, [items[0]]):
            for frag2 in _generate_all(grammar, items[1:]):
                for frag in _multiply(frag1, frag2):
                    frags.append(frag)
    return frags
            
def _multiply(frag1, frag2):
    frags = []
    if len(frag1) == 1:
        frag1 = [frag1]
    if len(frag2) == 1:
        frag2 = [frag2]
    for f1 in frag1:
        for f2 in frag2:
            frags.append(f1+f2)
    return frags

grammar = parse_cfg(
    """
    S -> NP VP
    NP -> Det N | Pro
    NP_PP -> Det N_PP
    PP -> P NP_PP
    VP -> V PP
    Det -> 'the'
    Det -> 'a'
    Pro -> 'he' | 'she' | 'they' | 'we'
    N -> 'man' | 'boy' | 'person' | 'woman' | 'girl'
    N_PP -> 'store' | 'supermarket'
    V -> 'went' | 'walked' | 'drove' | 'ran'
    P -> 'to'
    """)

for sent in generate(grammar):
    print ' '.join(sent)
    
