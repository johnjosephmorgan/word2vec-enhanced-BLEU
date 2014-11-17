import argparse

from gensim.models.word2vec import Word2Vec as w2v

from log_synonym_precision import log_synonym_precision
from brevity_penalty import brevity_penalty


def vleu(corpus, model, n):
    return log_synonym_precision(corpus, model, n) * brevity_penalty(corpus)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Standard BLEU')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-V', '--vectors', required=True,
                        help='Vectors file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    args = parser.parse_args()

    model = w2v.load_word2vec_format(fname=args.vectors, binary=True)

print vleu(args.corpus, model, args.precision)
