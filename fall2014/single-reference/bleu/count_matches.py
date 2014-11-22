from collections import Counter
import sys

from ngram_list import ngram_list


def count_matches(system, reference, n):
    counts = 0.0
    ng_refs = ngram_list(reference, n)
    for cand in ngram_list(system, n):
        if cand in ng_refs:
            counts += 1.0
            ng_refs.remove(cand)
        else:
            counts += 0.0

    return counts


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: count_matches.py SENTENCE REFERENCE N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
