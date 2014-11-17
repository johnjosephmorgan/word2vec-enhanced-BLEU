from collections import Counter
import sys

from ngrams import ngrams


def precision(system, reference, n):
    counts = Counter()
    p = 0.0
    ng_sys = ngrams(system, n)
    for ss in ng_sys:
        ng_refs = ngrams(reference, n)
        if ss in ng_refs:
            counts[ss] += ng_refs[ss]

    for ng in counts:
        p += float(counts[ng]) / float(len(system))
    return p

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'USAGE: precision.py SENTENCE N'
        exit()
    else:
        n = int(sys.argv[1])
        sysout = sys.argv[2].split()
        ref = sys.argv[3].split()
        out = precision(sysout, ref, n)
        print out
