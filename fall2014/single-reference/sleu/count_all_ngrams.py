from collections import Counter
import sys

from ngram_list import ngram_list


def count_all_ngrams(n, reference):
    ngram_count = 0
    ng_refs = ngram_list(reference, n)
    ngram_count += len(ng_refs)
    return ngram_count


if __name__ == '__main__':
    if len(sys.argv)  < 3:
        print 'USAGE: count_all_ngrams.py REFERENCE N'
        exit()

    n = int(sys.argv[1])
    ref = sys.argv[2:]

    out = count_all_ngrams(n, ref)
    print out
