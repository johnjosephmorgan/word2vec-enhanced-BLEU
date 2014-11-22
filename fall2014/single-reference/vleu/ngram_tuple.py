import sys


def ngram_tuple(sentence, n):
    """
    Returns the ngrams from a given sentence for a given n.
    """
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))
    ngrams = tuple()
    for start in range(0, len(sentence) - n + 1):
        ngrams = tuple(sentence[start:start + n])

    return ngrams

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'USAGE: ngram_tuple.py SENTENCE n'
        exit()
    else:
        sentence = sys.argv[1].split()
        n = int(sys.argv[2])
        out = ngram_tuple(sentence, n)
        print out
