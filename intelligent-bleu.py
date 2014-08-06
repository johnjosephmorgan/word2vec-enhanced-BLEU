import sys
import re
import string
from gensim.models.word2vec import Word2Vec as w2v

def get_alts(ref_ngram, ngram, model, numalts):
    """Returns a list of weights of the alternate n-grams generated.
    Alternate n-grams are guaranteed to match the argument ngram."""
    ind = -1
    alt_ngrams = []
    n = len(ref_ngram)

    for i in range(n):
        if not ref_ngram[i] == ngram[i]:
            if ind >= 0:    # Already found a mismatched word
                break       # So we need to get out of all of this
            ind = i
    else:   # Only found at most 1 mistmatched word
        if ind >= 0:    # Confirm we found 1, not 0 mismatched words
            try:
                alt_words = model.most_similar(positive=[ref_ngram[ind].lower()], topn=numalts)
            except KeyError:    # Out of dictionary word
                return []

            for pair in alt_words:
                if ngram[ind] == pair[0]:   # Found a match
                    # Weight = geometric mean of word distances
                    # So, b/c all but the new word have distance 1,
                    # it's just the nth root of dist(alt)
                    alt_ngrams.append(pair[1] ** (1/float(n)))
    return alt_ngrams


def ngrams(sentence, n):
    """Returns the ngrams from a given sentence for a given n."""
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))

    ngrams = []
    for start in range(0, len(sentence) - n + 1):
        ngrams.append(sentence[start:start + n])

    return ngrams


def bleu(N, references, output, model, numalts=2, threshold=0.0):
    """Performs the intelligent BLEU evaluation.
    N is the maximum precision
    references contains a list of sentences (arrays) that are the references
    output is a sentence (array) that is the output line
    model is the Word2Vec model to be used
    numalts is the number of alternate words to try, defaulting to 2
    threshold is the minimum cosine distance necessary for words to be considered similar, defaults to 0"""

    relevants = []
    counts = []
    for n in range(1, N + 1):
        output_ngrams = ngrams(output, n)
        reference_ngrams = []
        remove_helper = []
        relevant = 0.0

        # Build up reference_ngrams list, as well as an additional list
        # which is used to ensure proper removals
        for reference in references:
            temp = ngrams(reference, n)
            reference_ngrams += temp
            remove_helper.append(temp)

        for ngram in output_ngrams:
            if ngram in reference_ngrams:
                relevant += 1
                for reference in remove_helper:
                    if ngram in reference:
                        reference_ngrams.remove(ngram)
                        reference.remove(ngram)
            else:
                best_alt = None
                best_ref = None
                best_dist = threshold
                for ref_ngram in reference_ngrams:
                    for alt in get_alts(ref_ngram, ngram, model, numalts):
                        if alt > best_dist:
                            best_dist = alt
                            best_ref = ref_ngram

                # If we found a good alternative, count it and remove
                # the ngram it came from from the reference
                if best_dist > threshold:
                    # Mirror code above, add the distance instead of 1
                    relevant += best_dist
                    for reference in remove_helper:
                        if best_ref in reference:
                            reference_ngrams.remove(best_ref)
                            reference.remove(best_ref)

        relevants.append(relevant)
    return relevants


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print """error: Not enough arguments.
Usage: {} vector-file file-to-score [-a alternates] [-n precision] [-t threshold]
    vector-file: binary file of word2vec vectors
    file-to-score: file containing data to score, lines of the form "output ||| ref1 ||| ref2 ..."
    alternates: number of alternate words to try when doing replacement, integer, defaults to 2
    precision: maximum precision to use, integer, defaults to 4
    threshold: minimum closeness of word replacements, float, defaults to 0.0,
        using values greater than or equal to 1 effectively disables w2v""".format(sys.argv[0])
        exit()

    maxN = 4        # Maximum Precision
    nAlts = 2       # Number of alternate words to try
    thresh = 0.0    # Threshold of closeness
    rel_totals = [0.0] * maxN   # Total relevant for each precision
    count_totals = [0] * maxN   # Total word counts for each precision
    reflen = 0      # The length of the reference text
    corplen = 0     # The corpus length
    brevity = 1.0   # Brevity penalty, defaulting to 1.0
    const_e = 2.7182818     # Natural log base
    model = w2v.load_word2vec_format(fname=sys.argv[1], binary=True)

    try:
        for i in xrange(3, len(sys.argv), 2):
            if sys.argv[i] == "-a":
                nAlts = int(sys.argv[i+1])
            elif sys.argv[i] == "-n":
                maxN = int(sys.argv[i+1])
            elif sys.argv[i] == "-t":
                thresh = float(sys.argv[i+1])
            else:
                raise ValueError("Bad Argument")
    except ValueError:
        print "Bad argument: {}".format(" ".join(sys.argv[i:i+2]))
        exit()

    with open(sys.argv[2]) as f:
        for line in f:
            refs = []
            # Assumes the file has the pattern output ||| ref | ref...
            parts = line.split("|||")
            for p in parts[1:]:
                tmp = p.translate(string.maketrans("",""), string.punctuation)
                refs.append(tmp.split())  # Build up list of references
            outp = parts[0].split()
            rels = bleu(maxN, refs, outp, model, numalts=nAlts, threshold=thresh)  # BLEU step
            for i in range(maxN):
                rel_totals[i] += rels[i]
                count_totals[i] += max(0, len(outp) - i)
            # Add the length of the reference that is closest
            # (in absolute distance) to len(outp) to ref_len
            reflen += min([len(x) for x in refs], key=lambda y: abs(y - len(outp)))
            # And add len(outp) to corp_len
            corplen += len(outp)

    # Compute the product over all the precisions of, for each
    # precision, the total relevant score and total count
    # divide the sums for each precision
    placeholder = [(rel_totals[i] / count_totals[i]) for i in range(maxN)]
    # then take the geometric mean to get the score
    score = reduce(lambda x, y: x*y, placeholder) ** (1/float(maxN))

    if corplen < reflen:  # Calculate brevity penalty if necessary
        brevity = const_e ** (1 - (float(reflen) / corplen))

    # And finally, print the score multiplied by the brevity penalty
    for ind, obj in enumerate(placeholder):
        print "Precision: {}, Score: {}".format(ind+1, obj)
    print "Final Score: {}".format(score * brevity)
