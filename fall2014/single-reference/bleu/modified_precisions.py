from collections import Counter
import sys

from count_matches import count_matches
from count_all_ngrams import count_all_ngrams


def modified_precisions(corpus, history):
    total_ngrams = Counter()
    relevant_ngrams = Counter()
    precisions = Counter()

    with open(corpus) as f:
        for line in f:
            folds = line.split("|||")
            ref = folds[1].strip("\n").split()
            sys_out = folds[0].split()
            for hh in range(1, int(history) + 1):
                if hh <= len(ref):
                    total_ngrams[hh] += count_all_ngrams(hh, ref)
                    relevant_ngrams[hh] += count_matches(sys_out, ref, hh)
    for ii in relevant_ngrams.values():
        print ii,
    print '	',
    for ii in total_ngrams.values():
        print ii,
    print '	',
    for ii in range(1, int(history) + 1):
        precisions[ii] = float(relevant_ngrams[ii]) / float(total_ngrams[ii])
    for ii in precisions.values():
        print ii,
    print '	',
    return precisions

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: modified_precisions.py CORPUS HISTORY'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
    print modified_precisions(corpus, history)
