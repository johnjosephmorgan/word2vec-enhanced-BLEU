import sys
import re
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
                alt_words = model.most_similar(
                    positive=[ref_ngram[ind].lower()],
                    topn=numalts)
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
    """Implementation of BLEU-N automatic evaluation metric, with lambda=1
    using multiple references."""

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

        relevants.append(relevant)
    return relevants


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "error: Needs exactly 2 arguments, a binary vector file, and a file to score"
        
    maxN = 4    # Maximum Precision
    rel_totals = [0.0] * maxN   # Total relevant for each precision
    count_totals = [0] * maxN   # Total word counts for each precision
    reflen = 0      # The length of the reference text
    corplen = 0     # The corpus length
    brevity = 1.0   # Brevity penalty, defaulting to 1.0
    const_e = 2.7182818     # Natural log base
    model = w2v.load_word2vec_format(fname=sys.argv[1], binary=True)

    with open(sys.argv[2]) as f:
        for line in f:
            refs = []
            # Assumes the file has the pattern output ||| ref | ref...
            parts = re.split(string=line, pattern="\s*\|\|\|\s*")
            # parts = re.split(string=line, pattern="\s*\t\s*")
            for p in parts[1:]:
                refs.append(p.split())  # Build up list of references
            outp = parts[0].split()
            rels = bleu(maxN, refs, outp, model, numalts=5)  # BLEU step
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
