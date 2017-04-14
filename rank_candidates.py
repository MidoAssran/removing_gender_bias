from rf_word2vec import W2VResumeFilter
from feature_builder import construct_candidate_skills, load_alotaibi_users, load_alotaibi_jobs

def al_otaibi_resume_filter():
    """ Al Otaibi method """

    print("# -- Al Otaibi Resume Filter -- #")
    w2vrf = W2VResumeFilter(debiased=False)
    print("Loaded models")

    # Load users
    users_fname = "dummy.csv"
    user_profiles = load_alotaibi_users(users_fname)
    user_vectors = [construct_candidate_skills(u) for u in user_profiles]

    # Load jobs
    jobs_fname = "dummy.csv"
    job_profiles = load_alotaibi_jobs(jobs_fname)
    job_vectors = [w2vrf.get_word_centroid_vec(j) for j in job_profiles]

    cosine_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.cosine_filter_candidates(user_vectors, job_vector)
        cosine_job_ranks.append(ranks)
        print("cosine:", ranks)

    euclidean_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.euclidean_filter_candidates(user_vectors, job_vector)
        euclidean_job_ranks.append(ranks)
        print("euclidean:", ranks)

    jaccard_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.jaccard_filter_candidates(user_vectors, job_vector)
        jaccard_job_ranks.append(ranks)
        print("jaccard:", ranks)

    a = np.asarray(cosine_job_ranks)
    b = np.asarray(euclidean_job_ranks)
    c = np.asarray(jaccard_job_ranks)
    np.savetxt("cosine_ranks.csv", a, delimiter=",")
    np.savetxt("euclidean_ranks.csv", b, delimiter=",")
    np.savetxt("jaccard_ranks.csv", c, delimiter=",")


def w2v_resume_filter():
    """ W2V method """

    print("# -- Word  -- #")
    w2vrf = W2VResumeFilter(debiased=False)
    print("Loaded models")

    # Load users
    users_fname = "dummy.csv"
    users = w2vrf.load_candidates(users_fname)
    user_profiles, user_genders = users['candidates'], users['genders']
    user_vectors = [w2vrf.get_word_centroid_vec(u) for u in user_profiles]

    # Load jobs
    jobs_fname = "dummy.csv"
    job_profiles = w2vrf.load_jobs(jobs_fname)
    job_vectors = [w2vrf.get_word_centroid_vec(j) for j in job_profiles]

    cosine_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.cosine_filter_candidates(user_vectors, job_vector)
        cosine_job_ranks.append(ranks)
        print("cosine:", ranks)

    euclidean_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.euclidean_filter_candidates(user_vectors, job_vector)
        euclidean_job_ranks.append(ranks)
        print("euclidean:", ranks)

    jaccard_job_ranks = []
    for job_vector in job_vectors:
        ranks = w2vrf.jaccard_filter_candidates(user_vectors, job_vector)
        jaccard_job_ranks.append(ranks)
        print("jaccard:", ranks)

    a = np.asarray(cosine_job_ranks)
    b = np.asarray(euclidean_job_ranks)
    c = np.asarray(jaccard_job_ranks)
    np.savetxt("cosine_ranks.csv", a, delimiter=",")
    np.savetxt("euclidean_ranks.csv", b, delimiter=",")
    np.savetxt("jaccard_ranks.csv", c, delimiter=",")

def main():
    """ Main method """
    w2v_resume_filter()

if __name__ == "__main__":
    main()
