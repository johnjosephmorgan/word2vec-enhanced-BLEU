from collections import Counter
import math
import sys


def brevity_penalty(corpus):
    systems = []
    references = []
    r = 0
    c = 0
    with open(corpus) as f:
        for line in f:
            folds = line.split("|||")
            sys_out = folds[0].split()
            ref = folds[1].strip("\n").split()
            systems.append(sys_out)
            references.append(ref)

    for rr, cc in zip(references, systems):
        r += len(rr)
        c += len(cc)

    if c <= r:
        bp = math.exp((1 - r) / c)
    else:
        bp = 1.0

    return bp

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'USAGE: brevity_penalty.py CORPUS'
        exit()

    corpus = sys.argv[1]

    print brevity_penalty(corpus)
