import argparse

from brevity_penalty import brevity_penalty
from gmean_modified_precision import gmean_modified_precision


def bleu(corpus, n):
    print 'BLEU	',
    return gmean_modified_precision(corpus, n) * brevity_penalty(corpus)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Standard BLEU.')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    args = parser.parse_args()
    b = bleu(args.corpus, args.precision)
    print b

