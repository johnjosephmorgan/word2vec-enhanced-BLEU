from gensim import utils, matutils
from gensim.models.word2vec import Word2Vec
import numpy as np


def n_similarity(model, ws1, ws2):
    v1 = [model[word] for word in ws1]
    v2 = [model[word] for word in ws2]
    return np.dot(
        matutils.unitvec(np.array(v1).mean(axis=0)),
        matutils.unitvec(np.array(v2).mean(axis=0)))


