import argparse

from brevity_penalty import brevity_penalty
from gensim.models.word2vec import Word2Vec as w2v
from gmean_synonym_precision import gmean_synonym_precision


def xleu(corpus, model, method, threshold, precision=4):
    print method, 'bleu	',
    return gmean_synonym_precision(corpus, model, precision, method, threshold)\
        * brevity_penalty(corpus)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Cross ngram BLEU. Match jgrams with kgrams.')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-V', '--vectors', required=True,
                        help='Vectors file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    parser.add_argument('-t', '--threshold', type=float,
                        default=0.7, help='Similarity threshold. Only ngram pairs with similarity exceeding this threshold will be counted.')
    args = parser.parse_args()
    model = w2v.load_word2vec_format(fname=args.vectors, binary=True)
    for ii in ['x', 'v', 's']:
        xb = xleu(args.corpus, model, ii, args.threshold, args.precision)
        print xb
