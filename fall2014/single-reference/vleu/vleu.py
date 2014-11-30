import argparse

from brevity_penalty import brevity_penalty
from gensim.models.word2vec import Word2Vec as w2v
from gmean_synonym_precision import gmean_synonym_precision


def vleu(corpus, model, n):
    print 'VLEU	',
    return gmean_synonym_precision(corpus, model, n) * brevity_penalty(corpus)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Vector BLEU. Add similar ngram matche scores to precision.')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-V', '--vectors', required=True,
                        help='Vectors file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    args = parser.parse_args()

    model = w2v.load_word2vec_format(fname=args.vectors, binary=True)
    vb = vleu(args.corpus, model, args.precision)
    print vb
