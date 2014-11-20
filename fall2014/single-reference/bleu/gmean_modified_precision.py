import sys

from modified_precisions import modified_precisions
import numpy as np
from scipy.stats import gmean


def gmean_modified_precision(corpus, history):
    precisions = modified_precisions(corpus, history)
    return gmean(precisions.values())

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: log_modified_precision.py CORPUS HISTORY'
        exit()

    corpus = sys.argv[1]
    history = int(sys.argv[2])
    print log_modified_precision(corpus, history)
