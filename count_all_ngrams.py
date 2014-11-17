from collections import Counter
import sys

from ngrams import ngrams


def count_all_ngrams(n, reference):
    '''
    count total ngrams
    '''
    ngram_count = 0
    for rr in reference:
        ng_refs = ngrams(rr.split(), n)
        ngram_count += len(ng_refs)

    return ngram_count


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: count_all_ngrams.py N REFERENCE'
        exit()

    n = int(sys.argv[1])
    refs = sys.argv[2:]
    out = count_all_ngrams(n, refs)
    print out
