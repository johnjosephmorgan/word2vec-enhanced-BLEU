import math
import sys

from scipy.stats import gmean
from synonym_precisions import synonym_precisions


def gmean_synonym_precision(corpus, model, history):
    return gmean(synonym_precisions(corpus, model, history).values())


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'USAGE: log_synonym_precision.py CORPUS MODEL HISTORY'
        exit()

    corpus = sys.argv[1]
    model = sys.argv[2]
    history = int(sys.argv[3])
    print log_synonym_precision(corpus, model, history)
