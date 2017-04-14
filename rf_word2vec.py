import numpy as np
from scipy.spatial import distance
from gensim.models import KeyedVectors
from gensim.models import Word2Vec

class W2VResumeFilter:
    """
    A machine learning resume filter based on the case study in
        Al-Otaibi, "A survey of job recommender systems." 2013
    Extended to produce word vectors using google's word2vec and a debiased word2vec from
        Bolukbasi, "Man is to computer programmer as woman is to homemaker? ..." 2016.
    """

    HD_W2V_PATH = "./word2vec/GoogleNews-vectors-negative300-hard-debiased.bin.gz"
    W2V_PATH = "./word2vec/GoogleNews-vectors-negative300.bin.gz"

    def __init__(self, debiased=False):
        """ Constructor """
        if debiased:
            self.model = Word2Vec.load_word2vec_format(W2VResumeFilter.HD_W2V_PATH, binary=True)
        else:
            self.model = KeyedVectors.load_word2vec_format(W2VResumeFilter.W2V_PATH, binary=True)

    def get_word_centroid_vec(self, doc):
        """ Convert the document to a vector using the word centroid method """
        wcm = None
        for wrd in doc:
            if wcm is None:
                wcm = self.model[wrd]
            wcm += self.model[wrd]

        wcm /= float(len(doc))
        return wcm

    def cosine_filter_candidates(self, candidates, job):
        """ Filter candidates using the cosine similarity """

        scores = []
        for candidate in candidates:
            scores.append(distance.cosine(candidate, job))

        # Index list of best candidates sorted in descending order
        ranks = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

        return ranks

    def euclidean_filter_candidates(self, candidates, job):
        """ Filter candidates using the euclidean distance """

        scores = []
        for candidate in candidates:
            scores.append(distance.euclidean(candidate, job))

        # Index list of best candidates sorted in descending order
        ranks = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

        return ranks

    def jaccard_filter_candidates(self, candidates, job):
        """ Filter candidates using the jacard distance """

        scores = []
        for candidate in candidates:
            scores.append(distance.jaccard(candidate, job))

        # Index list of best candidates sorted in descending order
        ranks = sorted(range(len(scores)), key=lambda k: scores[k], reverse=True)

        return ranks

def main():
    """ Main method """
    w2vrf = W2VResumeFilter(debiased=True)

if __name__ == "__main__":
    print("# -- Main -- #")
    