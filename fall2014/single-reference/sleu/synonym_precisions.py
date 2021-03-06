from collections import Counter
import sys

from gensim.models.word2vec import Word2Vec as w2v

from count_synonyms import count_synonyms
from count_all_ngrams import count_all_ngrams


def synonym_precisions(corpus, model, history):
    total_ngrams = Counter()
    relevant_ngrams = Counter()
    precisions = Counter()

    with open(corpus) as f:
        for line in f:
            ref = []
            folds = line.split("|||")
            sys_out = folds[0].split()
            ref = folds[1].strip("\n").split()
            for hh in range(1, int(history) + 1):
                if hh <= len(ref):
                    total_ngrams[hh] += count_all_ngrams(hh, ref)
                    relevant_ngrams[hh] += count_synonyms(
                        sys_out, ref, model, hh)
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
    if len(sys.argv) != 4:
        print 'USAGE: synonym_precisions.py CORPUS MODEL HISTORY'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
    print synonym_precisions(corpus, model, history)
