from collections import Counter
import numpy as np
import sys

from gensim import utils, matutils
from gensim.models.word2vec import Word2Vec
from ngram_list import ngram_list


def n_similarity(model, ws1, ws2):
    v1 = [model[word] for word in ws1]
    v2 = [model[word] for word in ws2]
    return np.dot(
        matutils.unitvec(np.array(v1).mean(axis=0)),
        matutils.unitvec(np.array(v2).mean(axis=0)))


def count_synonyms(candidate, reference, model, n):
    matches = 0
    for cand_ngram in ngram_list(candidate, n):
        ng_refs = ngram_list(reference, n)
        if cand_ngram in ng_refs:
            matches += 1
        elif cand_ngram not in ng_refs:
            try:
                sims = []
                for ii in ng_refs:
                    sims.append(n_similarity(model, cand_ngram, ii))
                    if sims:
                        matches += np.mean(sims)
            except KeyError:
                matches += 0

    return matches


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'USAGE: count_synonyms.py SENTENCE REFERENCE MODEL N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
