from collections import Counter
import sys

from ngrams import ngrams
from counts_max_multiple_references import counts_max_multiple_references
from all_ngrams_multiple_references import all_ngrams_multiple_references


def precision_max_multiple_references_corpus(corpus, history):
    total_ngrams = Counter()
    total_rel_ngrams = Counter()
    precisions = Counter()

    with open(corpus) as f:
        for line in f:
            refs = []
            # Assumes the file has the pattern output ||| ref | ref...
            folds = line.split("|||")
            for rr in folds[1:]:
                refs.append(rr.strip("\n"))
            sys_out = folds[0].split()
            for hh in range(1, history + 1):
                total_ngrams[hh] += all_ngrams_multiple_references(hh, refs)
                total_rel_ngrams[hh] += counts_max_multiple_references(
                    sys_out, refs, hh)

    for ii in range(1, history + 1):
        precisions[ii] = float(total_ngrams[ii]) / float(total_rel_ngrams[ii])

    return precisions

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: precision_multiple_references_corpus.py file N'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
print precision_max_multiple_references_corpus(corpus, history)
