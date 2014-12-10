import math
import sys

from scipy.stats import gmean
from synonym_precisions import synonym_precisions


def gmean_synonym_precision(corpus, model, history, m):
    return gmean(synonym_precisions(corpus, model, history, m).values())


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'USAGE: log_synonym_precision.py CORPUS MODEL HISTORY METRIC'
        exit()

    corpus = sys.argv[1]
    model = sys.argv[2]
    history = int(sys.argv[3])
    m = int(sys.argv[4])
    print gmean_synonym_precision(corpus, model, history, m)
