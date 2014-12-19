from collections import Counter
import logging
import math
import sys

import numpy as np

from ngram_counter import ngram_counter
from ngram_list import ngram_list
from n_similarity import n_similarity

logging.basicConfig(
    filename='xleu_count_syns.log', level=logging.DEBUG)


def count_x_synonyms(candidate, reference, model, n, total_precision, threshold):
    matches = 0.0
    xng_refs = Counter()
    ng_refs = ngram_counter(reference, n)
    for ii in range(1, total_precision+1):
        xng_refs += ngram_counter(reference, ii)
    for cand in ngram_list(candidate, n):
        if tuple(cand) in ng_refs.keys():
            matches += 1.0
            ng_refs[tuple(cand)] -= 1.0
            xng_refs[tuple(cand)] -= 1.0
            if ng_refs[tuple(cand)] <= 0.0:
                del ng_refs[tuple(cand)]
            if xng_refs[tuple(cand)] <= 0.0:
                del xng_refs[tuple(cand)]
        elif tuple(cand) not in ng_refs.keys():
            try:
                sims = Counter()
                for rr in xng_refs.keys():
                    if rr:
                        sims[rr] = n_similarity(model, cand, rr)
                        if sims:
                            if float(np.max(sims.values())) > float(threshold):
                                matches += np.max(sims.values())
                                logging.info(
                                    '%s	%s	%f',\
                                    cand, max(sims), np.max(sims.values()))
                                xng_refs[max(sims)] -= sims[rr]
                                ng_refs[max(sims)] -= sims[rr]
                                if xng_refs[max(sims)] <= 0.0:
                                    del xng_refs[max(sims)]
                                if ng_refs[max(sims)] <= 0.0:
                                    del ng_refs[max(sims)]
            except KeyError:
                matches += 0.0

    return matches


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'USAGE: count_x_synonyms.py SENTENCE REFERENCE MODEL N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
