from collections import Counter
import math
import sys

from ngrams import ngrams
from counts_max_multiple_references import counts_max_multiple_references
from all_ngrams_multiple_references import all_ngrams_multiple_references
from modified_precisions import modified_precisions


def log_modified_precision(corpus, history):
    precisions = modified_precisions(corpus, history)
    weights = [1.0 / float(history)] * int(history)
    log_precision = 0.0
    for ww, pp in zip(weights, precisions):
        log_precision += ww * math.log(precisions[pp])

    return log_precision

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: log_modified_precision.py CORPUS HISTORY'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
    print log_modified_precision(corpus, history)
