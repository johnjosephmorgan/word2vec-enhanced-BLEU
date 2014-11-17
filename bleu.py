import argparse

from log_modified_precision import log_modified_precision
from brevity_penalty import brevity_penalty

def bleu(corpus, n):
    return log_modified_precision(corpus, n) * brevity_penalty(corpus)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Standard BLEU')
    parser.add_argument('-C', '--corpus', required=True,
                        help='Corpus file')
    parser.add_argument('-p', '--precision', metavar='int',
                        default=4, help='maximum precision')
    args = parser.parse_args()

print bleu(args.corpus, args.precision)
