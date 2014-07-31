#!/usr/bin/python

import sys
import re
import gensim.models.word2vec as w2v

def get_alts(ref_ngram, ngram, model, numalts):
    """Returns a list of weights of the alternate n-grams generated.
    Alternate n-grams are guaranteed to match the argument ngram."""
    ind = -1
    alt_ngrams = []
    n = len(ref_ngram)
    
    for i in range(n):
        if not ref_ngram[i] == ngram[i]:
            if ind >= 0:    # Already found a mismatched word, so we can't use this
                break
            ind = i
    else:   # Only found at most 1 mistmatched word
        if ind >= 0:    # Confirm we found 1, not 0 mismatched words
            try:
                alt_words = model.most_similar(positive=[ref_ngram[ind].lower()], topn=numalts)
            except KeyError:    # Out of dictionary word
                return []
            for pair in alt_words:
                if ngram[ind] == pair[0]:   # Found a match
                    alt_ngrams.append(pair[1] ** (1/float(n)))  # Weight = geometric mean of word distances
                
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
        
        for reference in references:    # Build up reference_ngrams list, as well as an additional list used to ensure proper removals
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
                for ref_ngram in reference_ngrams:
                    for alt in get_alts(ref_ngram=ref_ngram, ngram=ngram, model=model, numalts=numAlternatives):
                        if alt > best_dist:
                            best_dist = alt
                            best_ref = ref_ngram
                            
                if debug:
                    print "Close to: {}, Weight: {}".format(best_ref, best_dist)
                    
                # If we found a good alternative, count it and remove the ngram it came from from the reference
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
    maxN = 4    # Maximum Precision
    rel_totals = [0.0] * maxN   # Holds the total relevant scores for each precision
    count_totals = [0] * maxN   # Holds the total word counts for each precision
    ref_len = 0     # Holds the length of the reference text, w/ multiple refs this is as close to corp_len as possible
    corp_len = 0    # Hold the corpus length
    brevity = 1.0   # Brevity penalty, assumed to be 1.0 but recalculated later based on ref_len and corp_len
    const_e = 2.7182818     # Natural log base, this is more than enough sig figs for this
    model = w2v.Word2Vec.load_word2vec_format(fname=sys.argv[1], binary=True)   # gensim model

    with open(sys.argv[2]) as f:
        for line in f:
            refs = []
            parts = re.split(string=line, pattern="\s*\|+\s*")      # Assumes the file has the pattern output ||| ref | ref...
            for p in parts[1:]:
                refs.append(p.split())      # Build up list of references
            outp = parts[0].split()        
            rels = bleu(N=maxN, references=refs, output=outp, model=model, numAlternatives=5)  # Actual BLEU step
            for i in range(maxN):
                rel_totals[i] += rels[i]
                count_totals[i] += max(0, len(outp) - i)
            # Add the length of the reference that is closest (in absolute distance) to len(outp) to ref_len
            ref_len += min([len(x) for x in refs], key=lambda y: abs(y - len(outp)))
            # And add len(outp) to corp_len
            corp_len += len(outp)

    # Compute the product over all the precisions of, for each precision, the total relevant score and total count
    placeholder = [(rel_totals[i] / count_totals[i]) for i in range(maxN)]  # divide the sums for each precision
    score = reduce(lambda x,y: x*y, placeholder) ** (1/float(maxN))         # then take the geometric mean to get the score

    if corp_len < ref_len:  # Calculate brevity penalty if necessary
        brevity = const_e ** (1 - (float(ref_len) / corp_len))

    # And finally, print the score multiplied by the brevity penalty
    print "Final Score: {}".format(score * brevity)
