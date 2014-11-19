from collections import Counter
import math
import sys

from synonym_precisions import synonym_precisions


def log_synonym_precision(corpus, model, history):
    weights = [1.0 / float(history)] * int(history)
    log_precision = 0.0
    precisions = synonym_precisions(corpus, model, history)
    for ww, pp in zip(weights, precisions):
        if precisions[pp] > 0.0:
            log_precision += ww * math.log(precisions[pp])

    return log_precision

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'USAGE: log_synonym_precision.py CORPUS MODEL HISTORY'
        exit()

    corpus = sys.argv[1]
    model = sys.argv[2]
    history = int(sys.argv[3])
    print log_synonym_precision(corpus, model, history)
