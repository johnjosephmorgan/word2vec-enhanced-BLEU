from collections import Counter
import math
import sys


def closest(candidate, references):
    reference_lengths = Counter()
    if len(references) == 1:
        return references
    else:
        for rr in references:
            reference_lengths[rr] = math.fabs(
                float(len(rr.split())) - float(len(candidate.split())))
    return reference_lengths.most_common()[-1]

if __name__ == '__main__':
    print closest(sys.argv[1], sys.argv[2:])
