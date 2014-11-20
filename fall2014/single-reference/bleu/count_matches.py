from collections import Counter
import sys

from ngram_list import ngram_list


def count_matches(system, reference, n):
    '''
    given:
    word w from system output
    reference sentence r
    find occurrence of w in r
    sum over all w
    '''
    counts = Counter()
    for ww in ngram_list(system, n):
        if ww in ngram_list(reference, n):
            counts[str(ww)] += 1
        else:
            counts[str(ww)] += 0

    return sum(counts.values())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: count_matches.py SENTENCE REFERENCE N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
