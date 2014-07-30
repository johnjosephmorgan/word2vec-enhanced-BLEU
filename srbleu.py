#!/usr/bin/python

import fileinput
import sys
import re
import gensim.models.word2vec as w2v


def find_close(model, word, numalts):
    """Finds the [numalts] closest words to [word] according to word2vec"""
    try:
        return model.most_similar(positive=[word], topn=numalts)
    except KeyError:
        return None

        
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
        alt_words = find_close(model, mismatch_word.lower(), numalts)
        if alt_words != None:
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


def brevity_penalty(references, output):
    """Determine the length of the reference closest in length to the output"""
    assert len(references) > 0, "References empty!"
    reference_length = min([len(x) for x in references],
                           key= lambda y: y - len(output))
    brevity_penalty = min(1, float(len(output)) / reference_length)
    return brevity_penalty

    
def bleu(N, references, output, brevity=True, model=None, threshold=0.0, numAlternatives=2, debug=False):
    """Implementation of BLEU-N automatic evaluation metric, with lambda=1
    using multiple references."""
    
    precisions = []
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
                
        # If the output is too short, then we obviously didn't find anything
        # relevant
        if output_ngrams:
            precisions.append((relevant, len(output_ngrams)))
        else:
            precisions.append((0.0, len(output_ngrams)))
            
    #product = reduce(lambda x, y: x * y, precisions)
    
    if debug:
        print precisions
        
    """
    if brevity:
        return brevity_penalty(references, output) * product
    else:
        return product
    """
    return precisions

if __name__=="__main__":
    score_list = []
    model = w2v.Word2Vec.load_word2vec_format(fname=sys.argv[1], binary=True)

    for line in fileinput.input(sys.argv[2]):
        refs = []
        parts = re.split(string=line, pattern="\s*\|+\s*")
        for p in parts[1:]:
            refs.append(p.split())
        score_list.append(bleu(N=4, references=refs, output=parts[0].split(), brevity=False, model=model, numAlternatives=5, debug=False))
        
    fileinput.close()
    print score_list
