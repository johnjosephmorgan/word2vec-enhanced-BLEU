from collections import Counter
import math
import sys

from closest import closest


def closest_references(candidates, references_corpus):
    closest_refs = []
    for cand, refs in zip(candidates, references_corpus):
        closest_refs.append(closest(cand, refs))

    return closest_refs

if __name__ == '__main__':
    print closest_references(sys.argv[1], sys.argv[2:])
