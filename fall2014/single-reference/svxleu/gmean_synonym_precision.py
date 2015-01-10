import argparse
import math

from gensim.models.word2vec import Word2Vec as w2v

from scipy.stats import gmean
from synonym_precisions import synonym_precisions


def gmean_synonym_precision(corpus, model, history, m, threshold):
    return gmean(synonym_precisions(corpus, model, history, m,
                                    threshold).values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='compute geometric mean')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-V', '--vectors', required=True,
                        help='Vectors file')
    parser.add_argument('-e', '--metric', required=True,
                        help='metric')
    parser.add_argument('-p', '--precision', metavar='int',
                        required=False,
                        default=4, help='maximum precision')
    parser.add_argument('-t', '--threshold', type=float,
                        default=0.9,
                        help='Similarity threshold. \
                        Only ngram pairs with similarity exceeding this\
                        threshold will be counted.')
    args = parser.parse_args()
    model = w2v.load_word2vec_format(fname=args.vectors, binary=True)
    print gmean_synonym_precision(
        args.corpus, model, args.precision, args.metric, args.threshold)
