
from collections import Counter
import math
import sys

import numpy as np

from ngram_counter import ngram_counter
from ngram_list import ngram_list
from n_similarity import n_similarity



def count_v_synonyms(candidate, reference, model, n, threshold):
    matches = 0.0
    ng_refs = ngram_counter(reference, n)
    for cand in ngram_list(candidate, n):
        if tuple(cand) in ng_refs.keys():
            matches += 1.0
            ng_refs[tuple(cand)] -= 1.0
            if ng_refs[tuple(cand)] <= 0.0:
                del ng_refs[tuple(cand)]
        elif tuple(cand) not in ng_refs.keys():
            try:
                sims = Counter()
                for rr in ng_refs.keys():
                    sims[rr] = n_similarity(model, cand, rr)
                if sims:
                    if float(np.max(sims.values())) > float(threshold):
                        matches += np.max(sims.values())
                        ng_refs[max(sims)] -= sims[rr]
                        if ng_refs[max(sims)] <= 0.0:
                            del ng_refs[max(sims)]
            except KeyError:
                matches += 0.0

    return matches


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'USAGE: count_v_synonyms.py SENTENCE REFERENCE MODEL N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
