from collections import Counter
import numpy as np
import sys

from gensim import utils, matutils 
from gensim.models.word2vec import Word2Vec
from ngram_list import ngram_list


def n_similarity(model, ws1, ws2):
    v1 = [model[word] for word in ws1]
    v2 = [model[word] for word in ws2]
    return np.dot(matutils.unitvec(np.array(v1).mean(axis=0)), matutils.unitvec(np.array(v2).mean(axis=0)))




def count_synonyms(system, reference, model, n, threshold=0.5):
    counts = Counter()
    ng_sys = ngram_list(system, n)
    for ww in ng_sys:
        ng_refs = ngram_list(reference, n)
        if ww in ng_refs:
            counts[str(ww)] += 1
        else:
            try:
                for r_ng in ng_refs:
                    if len(r_ng) == 1:
                        syn = model.most_similar(positive=r_ng, topn=1)
                        if syn[0][0] in ww:
                            counts[str(ww)] += syn[0][1]
                    elif len(r_ng) > 1:
                        ng_similarity = n_similarity(model, ww, r_ng)
                        if ng_similarity > threshold:
                            counts[str(ww)] += ng_similarity
            except KeyError:
                counts[str(ww)] += 0

    return sum(counts.values())


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: count_matches.py SENTENCE REFERENCE N'
        exit()

    n = int(sys.argv[1])
    sysout = sys.argv[2].split()
    refs = sys.argv[3:]
    out = counts_max_multiple_references(sysout, refs, n)
    print out
