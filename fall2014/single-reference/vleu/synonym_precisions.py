from collections import Counter
import sys

from gensim.models.word2vec import Word2Vec as w2v

from count_synonyms import count_synonyms
from count_all_ngrams import count_all_ngrams


def synonym_precisions(corpus, model, history):
    total_ngrams = Counter()
    total_rel_ngrams = Counter()
    precisions = Counter()

    with open(corpus) as f:
        for line in f:
            refs = []
            folds = line.split("|||")
            sys_out = folds[0].split()
            refs = folds[1].strip("\n").split()
            for hh in range(1, int(history) + 1):
                total_ngrams[hh] += count_all_ngrams(hh, refs)
                total_rel_ngrams[hh] += count_synonyms(
                    sys_out, refs, model, hh)
    for ii in range(1, int(history) + 1):
        precisions[ii] = float(total_rel_ngrams[ii]) / float(total_ngrams[ii])

    return precisions

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'USAGE: synonym_precisions.py CORPUS MODEL HISTORY'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
    print synonym_precisions(corpus, model, history)
