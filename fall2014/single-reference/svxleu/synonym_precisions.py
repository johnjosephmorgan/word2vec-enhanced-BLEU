import argparse
from collections import Counter

from gensim.models.word2vec import Word2Vec as w2v

from count_s_synonyms import count_s_synonyms
from count_v_synonyms import count_v_synonyms
from count_x_synonyms import count_x_synonyms
from count_all_ngrams import count_all_ngrams


def synonym_precisions(corpus, model, history, m, threshold):
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
                    if m == 's':
                        relevant_ngrams[hh] += count_s_synonyms(
                            sys_out, ref, model, hh, threshold)
                    elif m == 'v':
                        relevant_ngrams[hh] += count_v_synonyms(
                            sys_out, ref, model, hh, threshold)
                    elif m == 'x':
                        relevant_ngrams[hh] += count_x_synonyms(
                            sys_out, ref, model, hh, history, threshold)

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
    parser = argparse.ArgumentParser(
        description='compute precisions')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-V', '--vectors', required=True,
                        help='Vectors file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    parser.add_argument('-t', '--threshold', type=float,
                        default=0.7, help='Similarity threshold. Only ngram pairs with similarity exceeding this threshold will be counted.')
    parser.add_argument('-e', '--metric', required=True,
                        help='metric')

    args = parser.parse_args()
    model = w2v.load_word2vec_format(fname=args.vectors, binary=True)
    print synonym_precisions(
        args.corpus, model, args.precision, args.metric, args.threshold)
