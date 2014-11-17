from collections import Counter
import sys

from ngrams import ngrams
from gensim.models.word2vec import Word2Vec as w2v


def count_synonyms(system, reference, model, n):
    ng_sys = ngrams(system, n)
    counts = Counter()
    for ww in ng_sys:
        ng_refs = ngrams(str(reference).split(), n)
        if ww in ng_refs:
            counts[ww] = ng_refs[ww]
        else:
            try:
                syn_ngrams = model.most_similar(positive=[ww], topn=10)
                counts[ww] = syn_ngrams
            except KeyError:
                counts[ww] = 0

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
