from collections import Counter
import math
import sys

from closest_references import closest_references


def brevity_penalty(corpus):
    systems = []
    references = []
    r = 0
    c = 0
    with open(corpus) as f:
        for line in f:
            refs = []
            folds = line.split("|||")
            for rr in folds[1:]:
                refs.append(rr.strip("\n"))

            sys_out = folds[0].split()
            references.append(refs)
            systems.append(sys_out)

    best_refs = closest_references(systems, references)
    for rr, cc in zip(best_refs, systems):
        ss = str(rr)
        tt = ss.split()
        cs = str(cc)
        dd = cs.split()
        r += len(tt)
        c += len(dd)

    if c <= r:
        bp = math.exp((1 - r) / c)
    else:
        bp = 1.0

    return (-1.0) * bp

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: brevity_penalty.py CORPUS'
        exit()

    corpus = sys.argv[1]

    print brevity_penalty(corpus)
