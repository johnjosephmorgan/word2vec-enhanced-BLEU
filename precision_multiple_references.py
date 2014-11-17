from collections import Counter
import sys

from ngrams import ngrams


def precision_multiple_references(system, references, n):
    counts = Counter()
    p = 0.0
    ng_sys = ngrams(system, n)
    for ss in ng_sys:
        for rr in references:
            ng_refs = ngrams(rr.split(), n)
            if ss in ng_refs:
                counts[ss] += ng_refs[ss]

    print counts
    for ng in counts:
        p += float(counts[ng]) / float(len(system))
    return p

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: precision_multiple_references.py SENTENCE REFERENCES N'
        exit()
    else:
        n = int(sys.argv[1])
        sysout = sys.argv[2].split()
        refs = sys.argv[3:]
        out = precision_multiple_references(sysout, refs, n)
        print out
