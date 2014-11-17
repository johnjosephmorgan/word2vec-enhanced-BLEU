from collections import Counter
import sys

from ngrams import ngrams


def counts_max_multiple_references(system, references, n):
    '''
    given:
    word ww from system output
    reference sentences r1 r2 r3 r4
    ww occurrs o1 times in r1 o2 in r2 o3 in r3 o4 in r4
    find max of o1 o2 o3 o4
    sum over all ww
    '''
    max_word_count = Counter()
    ng_sys = ngrams(system, n)
    for ww in ng_sys:
        counts = Counter()
        for rr in references:
            ng_refs = ngrams(rr.split(), n)
            if ww in ng_refs:
                counts[rr] = ng_refs[ww]
            else:
                counts[rr] = 0

        max_word_count[ww] = max(counts.values())

    return sum(max_word_count.values())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: counts_multiple_references.py SENTENCE REFERENCES N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
