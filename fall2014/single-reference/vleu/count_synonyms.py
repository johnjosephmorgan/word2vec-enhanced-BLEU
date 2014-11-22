from collections import Counter
import sys

from gensim import utils, matutils
from gensim.models.word2vec import Word2Vec
import numpy as np

from ngram_counter import ngram_counter
from ngram_list import ngram_list



def n_similarity(model, ws1, ws2):
    v1 = [model[word] for word in ws1]
    v2 = [model[word] for word in ws2]
    return np.dot(
        matutils.unitvec(np.array(v1).mean(axis=0)),
        matutils.unitvec(np.array(v2).mean(axis=0)))


def count_synonyms(candidate, reference, model, n):
    matches = 0.0
    ng_refs = ngram_counter(reference, n)
    for cand_ngram in ngram_list(candidate, n):
        if tuple(cand_ngram) in ng_refs.keys():
            matches += 1.0
            del ng_refs[tuple(cand_ngram)]
        elif tuple(cand_ngram) not in ng_refs.keys():
            try:
                sims = []
                for rr in ng_refs.keys():
                    sims.append( n_similarity(model, cand_ngram, rr))
                    if sims:
                        matches += np.max(sims)
                        del ng_refs[rr]
            except KeyError:
                matches += 0.0

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
