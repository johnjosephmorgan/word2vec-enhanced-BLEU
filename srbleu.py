#!/usr/bin/python

import fileinput
import sys
import re
import gensim.models.word2vec as w2v

def get_alts(ref_ngram, ngram, model, numalts):
    """Return a list of alternates for ref_ngram"""
    inds = []   # This is done so multi-replacement can be implemented later if desired
    alt_ngrams = []
    n = len(ref_ngram)
    for i in range(n):
        if not ref_ngram[i] == ngram[i]:
            inds.append(i)
    if len(inds) == 1:
        mismatch_word = ref_ngram[inds[0]]
        try:
            alt_words = model.most_similar(positive=[mismatch_word.lower()], topn=numalts)
        except KeyError:
            return []
        for pair in alt_words:
            if ngram[inds[0]] == pair[0]:
                prefix = ref_ngram[:inds[0]]
                postfix = ref_ngram[inds[0] + 1:]
                alt = prefix + [pair[0]] + postfix
                weight = pair[1] ** (1/float(n))
                # weight is the geometric mean of the word distances,
                # which, because only the changed word has a distance not
                # equal to 1, is just the nth root of the distance
                alt_ngrams.append((alt, weight, ref_ngram))
    return alt_ngrams
    
    
def ngrams(sentence, n):
    """Returns the ngrams from a given sentence for a given n."""
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))

    ngrams = []
    for start in range(0, len(sentence) - n + 1):
        ngrams.append(sentence[start:start + n])

    return ngrams

    
def bleu(N, references, output, model=None, threshold=0.0, numAlternatives=2, debug=False):
    """Implementation of BLEU-N automatic evaluation metric, with lambda=1
    using multiple references."""
    
    relevants = []
    counts = []
    for n in range(1, N + 1):
        output_ngrams = ngrams(output, n)
        reference_ngrams = []
        remove_helper = []
        relevant = 0.0
        for reference in references:
            temp = ngrams(reference, n)
            reference_ngrams += temp
            remove_helper.append(temp)
        for ngram in output_ngrams:
            if debug:
                print "Looking for: {}".format(ngram)
                print "In: {}".format(reference_ngrams)
            if ngram in reference_ngrams:
                relevant += 1
                for reference in remove_helper:
                    if ngram in reference:
                        reference_ngrams.remove(ngram)
                        reference.remove(ngram)
                if debug:
                    print "Found: {}".format(ngram)
            else:
                if debug:
                    print "Not Found: {}".format(ngram)
                best_alt = None
                best_ref = None
                best_dist = threshold
                alt_ngrams = []
                for ref_ngram in reference_ngrams:
                    alt_ngrams += get_alts(ref_ngram=ref_ngram, ngram=ngram, model=model, numalts=numAlternatives)
                for alt in alt_ngrams:
                    if alt[0] == ngram and alt[1] > best_dist:
                        best_alt = alt[0]
                        best_dist = alt[1]
                        best_ref = alt[2]
                # If we found a good alternative, count it and remove the ngram it came from from the reference
                if debug:
                    print "Using: {}, weight: {}, from:{}".format(best_alt, best_dist, best_ref)
                if best_dist > threshold:
                    relevant += best_dist       # Mirror code above, add the distance instead of 1
                    for reference in remove_helper:
                        if best_ref in reference:
                            reference_ngrams.remove(best_ref)
                            reference.remove(best_ref)

        relevants.append(relevant)

    if debug:
        print relevants

    return relevants

if __name__=="__main__":
    maxN = 4
    rel_totals = [0.0] * maxN
    count_totals = [0] * maxN
    ref_len = 0
    corp_len = 0
    product = 1.0
    brevity = 1.0
    const_e = 2.7182818     # more than enough sig figs for this
    model = w2v.Word2Vec.load_word2vec_format(fname=sys.argv[1], binary=True)

    with open(sys.argv[2]) as f:
        for line in f:
            refs = []
            parts = re.split(string=line, pattern="\s*\|+\s*")
            for p in parts[1:]:
                refs.append(p.split())
            outp = parts[0].split()        
            rels = bleu(N=maxN, references=refs, output=outp, model=model, numAlternatives=5, debug=False)
            for i in range(maxN):
                rel_totals[i] += rels[i]
                count_totals[i] += max(0, len(outp) - i)
            # Finally, work out what to add to the total reference length and corpus length
            # Add the length of the reference that is closest (in absolute distance) to len(outp) to ref_len
            ref_len += min([len(x) for x in refs], key=lambda y: abs(y - len(outp)))
            # And add len(outp) to corp_len
            corp_len += len(outp)

    # Compute the product over all the precisions of, for each precision, the total relevant score and total count
    for i in range(maxN):
        product *= (rel_totals[i] / count_totals[i])

    if corp_len < ref_len:  # Apply brevity penalty
        brevity = const_e ** (1 - (float(ref_len) / corp_len))
        
    print "Final Score: {}".format((product ** (1/float(maxN))) * brevity)
