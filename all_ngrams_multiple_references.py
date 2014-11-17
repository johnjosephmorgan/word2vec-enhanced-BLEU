from collections import Counter
import sys

from ngrams import ngrams


def all_ngrams_multiple_references(n, references):
    '''
    count total ngrams
    '''
    ngram_count = 0
    for rr in references:
        ng_refs = ngrams(rr.split(), n)
        ngram_count += len(ng_refs)

    return ngram_count


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: all_ngrams_multiple_references.py N REFERENCES'
        exit()

    n = int(sys.argv[1])
    refs = sys.argv[2:]
    out = all_ngrams_multiple_references(n, refs)
    print out
