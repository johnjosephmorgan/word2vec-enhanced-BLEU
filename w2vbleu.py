
import fileinput
import sys

from gensim.models import Word2Vec


def find_close(word, numalts, model):
    """
    Finds the [numalts] closest words to [word] according to word2vec
    """
    closest = model.most_similar(word)
    return closest[:numalts]


def ngrams(sentence, n):
    """
    Returns the ngrams from a given sentence for a given n.
    """
    assert isinstance(sentence, list), "Sentences are lists, got %s: %s" \
        % (str(type(sentence)), str(sentence))

    ngrams = []
    for start in range(0, len(sentence) - n + 1):
        ngrams.append(sentence[start:start + n])

    return ngrams


def brevity_penalty(references, output):
    '''
    Determine the length of the reference closest in length to the output
    '''
    assert len(references) > 0, "References empty!"
    reference_length = min([len(x) for x in references],
                           key=lambda y: y - len(output))
    brevity_penalty = min(1, float(len(output)) / reference_length)
    return brevity_penalty


def exact_match(ngram, reference_ngrams):
    if ngram in reference_ngrams:
        return True
    else:
        return None


def get_precision(n, references,
                  num_alternatives, threshold, model, output_ngrams):
    '''
    compute precision for sequences of length n
    '''
    relevant = 0
    for ngram in output_ngrams:
        for reference in references:
            reference_ngrams = ngrams(reference, n)
            if exact_match(ngram, reference_ngrams):
                relevant += 1

        for reference in references:
            reference_ngrams = ngrams(reference, n)
            best_dist = 0.0
            alt_ngrams = []
            for ref_ngram in reference_ngrams:
                differs_by_one = 0
                ind = 0
                for i in range(n):
                    if ref_ngram[i].lower() == ngram[i].lower():
                        differs_by_one += 1
                    else:
                        ind = i

                if differs_by_one == n-1:
                    one_off_ngram = ref_ngram[ind].lower()
                    alt_words_score = find_close(one_off_ngram,
                                                 num_alternatives, model)

                    if alt_words_score is None:
                        continue

                    for key in alt_words_score:
                        prefix_gram = ref_ngram[:ind]
                        suffix_gram = ref_ngram[ind+1:]
                        new_ngram = prefix_gram + [str(key[0])] + suffix_gram
                        alt_ngrams.append((new_ngram, key[1]))

                    for alt in alt_ngrams:
                        if alt[1] > best_dist:
                            best_dist = alt[1]

        if best_dist >= threshold:
            relevant += best_dist

    return relevant


def bleu(N, references, output,         brevity=True, threshold=0.0,
         num_alternatives=2, model=None):
    """
    Implementation of BLEU-N automatic evaluation metric, with lambda=1
ain    using multiple references.
    """
    precisions = []

    for n in range(1, N + 1):
        output_ngrams = ngrams(output, n)
        precision = get_precision(n, references, num_alternatives, threshold,
                                  model, output_ngrams)
        if output_ngrams and precision > 0:
            precisions.append(float(precision) / len(output_ngrams))
        else:
            pass

    product = reduce(lambda x, y: x * y, precisions)

    if brevity:
        return brevity_penalty(references, output) * product
    else:
        return product

if __name__ == "__main__":
    if len(sys.argv) > 2:
        reference_file = sys.argv[1]
        mt_output_file = sys.argv[2]
    else:
        print 'USAGE: sys.argv[0] REFERENCE_FILE MT_OUTPUT_FILE'

    score_list = {}
    refs = []

    for line in open(reference_file).readlines():
        refs.append(line.strip("\n").split())

    model = Word2Vec.load_word2vec_format('./vectors.bin', binary=True)

    for line in open(mt_output_file).readlines():
        score_list[line.strip("\n")] = bleu(N=4, references=refs,
                                            output=line.strip("\n").split(), brevity=True,
                                            model=model)

    print 'score', score_list
