from collections import Counter
import sys

from ngram_list import ngram_list


def count_all_xgrams(n, reference):
    ngram_count = 0
    for ii in range(1, 4):
        ng_refs = ngram_list(reference, ii)
        ngram_count += len(ng_refs)
    return ngram_count


if __name__ == '__main__':
    if len(sys.argv)  < 3:
        print 'USAGE: count_all_xgrams.py REFERENCE N'
        exit()

    n = int(sys.argv[1])
    ref = sys.argv[2:]

    out = count_all_xgrams(n, ref)
    print out
