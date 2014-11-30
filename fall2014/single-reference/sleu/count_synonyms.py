from collections import Counter
import logging
import math
import sys

from ngram_counter import ngram_counter
from ngram_list import ngram_list
import numpy as np
from n_similarity import n_similarity


logging.basicConfig(
    filename='sleu_count_syns.log', level=logging.DEBUG)


def count_synonyms(candidate, reference, model, n):
    matches = 0.0
    ng_refs = ngram_counter(reference, n)
    for cand in ngram_list(candidate, n):
        if tuple(cand) in ng_refs.keys():
            matches += 1.0
            ng_refs[tuple(cand)] -= 1.0
            if ng_refs[tuple(cand)] <= 0.0:
                del ng_refs[tuple(cand)]
        elif tuple(cand) not in ng_refs.keys():
            if n == 1:
                logging.info(
                    "no exact match for %s in %s",\
                    str(cand), str(ng_refs.keys()))
                try:
                    sims = Counter()
                    for rr in ng_refs.keys():
                        sims[rr] = math.fabs(n_similarity(model, cand, rr))
                        logging.info(
                            "similarity between %s and %s is %f",\
                            cand, rr, sims[rr])
                    if sims:
                        logging.info(
                            "match count for %s before incrementing is %f",\
                            str(cand[0]), matches)
                        matches += np.max(sims.values())
                        logging.info(
                            "%s matched %s count incremented by %f yield  %f",\
                            str(cand[0]), str(max(sims)), sims[rr], matches)
                        ng_refs[max(sims)] -= sims[rr]
                        if ng_refs[max(sims)] == 0.0:
                            logging.info(
                                "removing %s from %s", str(max(sims)), ng_refs)
                            del ng_refs[max(sims)]
                            logging.info(
                                "yields %s", ng_refs)
                except KeyError:
                    matches += 0.0
            elif            n > 1:
                matches += 0.0
    return matches


if __name__ == '__main__':
    logging.basicConfig(
        filename='sleu_count_syns.log', level=logging.DEBUG)

    if len(sys.argv) != 5:
        print 'USAGE: count_synonyms.py SENTENCE REFERENCE MODEL N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
