from collections import Counter
import sys


def ngrams(sentence, n):
    """
    Returns the ngrams from a given sentence for a given n.
    """
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))
    ngrams = Counter()
    for start in range(0, len(sentence) - n + 1):
        ngrams[str(sentence[start:start + n])] += 1
    return ngrams

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: ngrams.py SENTENCE n'
        exit()
    else:
        sentence = sys.argv[1].split()
        n = int(sys.argv[2])
        out = ngrams(sentence, n)
        print out
