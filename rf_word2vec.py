import numpy as np
from scipy.spatial import distance
from gensim.models import KeyedVectors

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
            self.model = KeyedVectors.load_word2vec_format(W2VResumeFilter.HD_W2V_PATH, binary=True)
        else:
            self.model = KeyedVectors.load_word2vec_format(W2VResumeFilter.W2V_PATH, binary=True)


    def get_word_centroid_vec(self, doc):
        """ Convert the document to a vector using the word centroid method """
        wcm = None
        for wrd in doc:
            try:
                vec = self.model[wrd]
            except:
                continue

            if wcm is None:
                wcm = vec
            wcm += vec

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

        # Index list of best candidates sorted (best first)
        ranks = sorted(range(len(scores)), key=lambda k: scores[k], reverse=False)

        return ranks

    def jaccard_filter_candidates(self, candidates, job):
        """ Filter candidates using the jacard distance """

        scores = []
        for candidate in candidates:
            scores.append(distance.jaccard(candidate, job))

        # Index list of best candidates sorted (best first)
        ranks = sorted(range(len(scores)), key=lambda k: scores[k], reverse=False)

        return ranks

    def load_jobs(self, filename):
        """ Load the jobs from the target file """
        # For now just return dummy list

        jobs = [
            ["Computer", "science", "software", "data", "science", "engineering", "junior", "engineer"],
            ["Computer", "hardware", "circuit", "data", "science", "engineering", "junior", "engineer"],
            ["Computer", "hardware", "electrical", "data", "science", "engineering", "junior", "engineer"]
        ]

        return jobs

    def load_candidates(self, filename):
        """ Load the jobs from the target file """
        # For now just return dummy list

        candidates = [
            ["she", "she", "she", "computer", "science", "Harvard"],
            ["he", "he", "he", "computer", "science", "Harvard"],
            ["she", "she", "computer", "science", "Harvard"],
            ["he", "he", "computer", "science", "Harvard"],
            ["she", "computer", "science", "Harvard"],
        ]

        candidate_genders = [
            "F", "M", "F", "M", "F"
        ]

        return {"candidates": candidates, "genders": candidate_genders}

def main():
    """ Main method """

    print("# -- Main -- #")
    w2vrf = W2VResumeFilter(debiased=False)
    print("Here")

    users = w2vrf.load_candidates("dummy.csv")
    user_profiles, user_genders = users['candidates'], users['genders']
    job_profiles = w2vrf.load_jobs("dummy_j.csv")
    print(user_profiles)
    print(job_profiles)

    user_vectors = [w2vrf.get_word_centroid_vec(u) for u in user_profiles]
    job_vectors = [w2vrf.get_word_centroid_vec(j) for j in job_profiles]

    ranks = w2vrf.cosine_filter_candidates(user_vectors, job_vectors)
    print(ranks)

if __name__ == "__main__":
    main()
