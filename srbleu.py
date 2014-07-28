#!/usr/bin/python

# INSERTED CODE BEGINS, these are some new constants and imports
import subprocess
import fileinput
import sys
import gensim.models.word2vec as w2v

createVectorsCmd = "./build-on-data.sh"
getCloseCmd = "./get-top-words.sh"
# INSERTED CODE ENDS

references = ["Israeli officials are responsible for airport security".split(),
        "Israel is in charge of the security at this airport".split(),
        """The security work for this airport is the responsibility of the
        Israel government""".split(),
        "Israeli side was in charge of the security of this airport".split()]
system_a = "Israeli officials responsibility of airport safety".split()
system_b = "airport security Israeli officials are responsible".split()

# INSERTED CODE BEGINS, this is a function for finding the close words
def find_close(word, numalts, gensim=False):
    """Finds the [numalts] closest words to [word] according to word2vec"""
    if gensim:
        model = w2v.Word2Vec.load_word2vec_format('./dataset.vectors.bin', binary=True)
        try:
            return model.most_similar(positive=[word], topn=numalts)
        except KeyError:
            return None

    proc = subprocess.Popen([getCloseCmd, word, str(numalts)], stdout=subprocess.PIPE)
    table = proc.stdout.read().split("\n")[-1 - numalts:-1]
    if "Out of dictionary word!" in table:
        return None
    words_weights = []
    for line in table:
        parts = line.split()
        words_weights.append((parts[0], float(parts[1])))
    return words_weights
# INSERTED CODE ENDS

# INSERTED COD BEGINS, this is a function that finds alternatives
def get_alts(ref_ngram, ngram, numalts, multi_rep=False):
    inds = []
    alt_ngrams = []
    n = len(ref_ngram)
    for i in range(n):
        if not ref_ngram[i] == ngram[i]:
            inds.append(i)
    if len(inds) == 1 or (multi_rep and n == 4 and len(inds) == 2):
        for ind in inds:
            alt_words = find_close(ref_ngram[ind].lower(), numalts)
            if not alt_words == None:
                for pair in alt_words:
                    alt_ngrams.append((ref_ngram[:ind] + [pair[0]] + ref_ngram[ind+1:], pair[1] ** (1/float(n))))
    return alt_ngrams
# INSERTED CODE ENDS
    
def ngrams(sentence, n):
    """Returns the ngrams from a given sentence for a given n."""
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))

    ngrams = []
    for start in range(0, len(sentence) - n + 1):
        ngrams.append(sentence[start:start + n])

    return ngrams


def brevity_penalty(references, output):
    # Determine the length of the reference closest in length to the output
    assert len(references) > 0, "References empty!"
    reference_length = min([len(x) for x in references],
                           key= lambda y: y - len(output))
    brevity_penalty = min(1, float(len(output)) / reference_length)
    return brevity_penalty

# MODIFIED CODE BEGINS, added additional parameters to this function
def bleu(N, references, output, brevity=True, use_w2v=False, threshold=0.0, numAlternatives=2):
# MODIFIED CODE ENDS
    """Implementation of BLEU-N automatic evaluation metric, with lambda=1
    using multiple references."""
    
    precisions = []
    for n in range(1, N + 1):
        output_ngrams = ngrams(output, n)
        relevant = 0.0
        for ngram in output_ngrams:
            for reference in references:
                reference_ngrams = ngrams(reference, n)
                if ngram in reference_ngrams:
                    relevant += 1
                    reference_ngrams.remove(ngram)
                    break
                # INSERTED CODE BEGINS, this finds the alternatives, selects the best, and updates the reference ngrams and relevant count
                elif use_w2v:
                    best_dist = 0.0
                    alt_ngrams = []
                    for ref_ngram in reference_ngrams:
                        alt_ngrams += get_alts(ref_ngram=ref_ngram, ngram=ngram, numalts=numAlternatives, multi_rep=False)
                    for alt in alt_ngrams:
                        if alt[0] == ngram:
                            best_dist = alt[1]
                            break
                    # If we found a good alternative, count it and remove the ngram it came from from the reference
                    if best_dist > threshold:
                        relevant += best_dist       # Mirror code above, add the distance instead of 1
                        reference_ngrams.remove(ref_ngram)
                        break
                # INSERTED CODE ENDS NOW               

        # If the output is too short, then we obviously didn't find anything
        # relevant
        if output_ngrams:
            precisions.append(float(relevant) / len(output_ngrams))
        else:
            precisions.append(0.0)

    product = reduce(lambda x, y: x * y, precisions)

    if brevity:
        return brevity_penalty(references, output) * product
    else:
        return product

# INSERTED CODE BEGINS, this is a new front end to make this a useable program
def main():
    #subprocess.call(createVectorsCmd)
    score_list = {}
    refs = []

    for line in fileinput.input("reference"):
        refs.append(line.split())
        
    fileinput.close();
    
    for line in fileinput.input("mt-output"):
        score_list[line] = bleu(N=4, references=refs, output=line.split(), brevity=True, use_w2v=True)
        
    print score_list

if __name__=="__main__":
    main()
# INSERTED CODE ENDS
