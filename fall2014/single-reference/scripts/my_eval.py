from nltk import nonterminals, Production, parse_cfg
import generate
# Create some nonterminals
S, NP, VP, PP = nonterminals('S, NP, VP, PP')
N, V, P, Det = nonterminals('N, V, P, Det')
VP_slash_NP = VP/NP
# Create some Grammar Productions
grammar = parse_cfg(
    """
    S -> NP VP
    PP -> P NP
    NP -> Det N | NP PP
    VP -> V NP | VP PP
    Det -> 'a' | 'the'
    N -> 'boy' | 'girl'
    V -> 'chased' | 'sat'
    P -> 'on' | 'in' | 'to'
    """)

