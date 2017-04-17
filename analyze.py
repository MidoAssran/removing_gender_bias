from collections import Counter
import csv
import numpy as np
import matplotlib.pyplot as plt

folder = "./data/"
fnames = ["_cosine_genders_alotaibi.csv",
          "_euclidean_genders_alotaibi.csv",
          "_jaccard_genders_alotaibi.csv",
          "True_euclidean_ranks_g.csv",
          "False_euclidean_ranks_g.csv",
          "True_cosine_ranks_g.csv",
          "False_cosine_ranks_g.csv",
          "False_jaccard_ranks_g.csv"]

fnames_method = ["Baseline Cosine",
                 "Basline Euclidean",
                 "Baseline Jaccard",
                 "Debiased Euclidean",
                 "Euclidean",
                 "Debiased Cosine",
                 "Cosine",
                 "Jaccard"]

male = "male"
female = "female"

top_n_list = [1, 10, 100, 1000, 5000]
def compute_results(top_n_results):

    # Loop through the top_n to compute
    for top_n in top_n_list:

        # Loop through the methods
        metrics = []
        for fname in fnames:
            f = open(folder + fname, 'r')
            reader = csv.reader(f)

            # Loop through the jobs for a given method
            jobs = []
            for row in reader:
                row_n = row[:top_n]
                count = Counter(row_n)
                m_count = count[male]
                f_count = count[female]
                # try:
                #     m2f = float(m_count) / float(f_count)
                # except:
                #     m2f = 1.0
                # jobs.append(m2f)
                jobs.append((m_count, f_count))

            metrics.append(jobs)

        # dict_scores = {}
        # for i, jobs in enumerate(metrics):
        #     method_name = fnames_method[i]
        #     print(method_name)
        #     avg = np.mean(jobs)
        #     std = np.std(jobs)
        #     dict_scores[method_name] = {"avg": avg, "std": std}
        #     print("\t", avg, std)
        # top_n_results.append(dict_scores)
        top_n_results.append(metrics)

    # return top_n_results

def plot(results, c, t):
    male_means = []
    male_stds = []
    female_means = []
    female_stds = []
    for method in results:
        male_counts = [job[0] for job in method]
        female_counts = [job[1] for job in method]
        m_avg = np.mean(male_counts)
        m_std = np.std(male_counts)
        f_avg = np.mean(female_counts)
        f_std = np.std(female_counts)
        male_means.append(m_avg)
        female_means.append(f_avg)
        male_stds.append(m_std)
        female_stds.append(f_std)

    ind = np.arange(len(fnames_method))
    width = 0.35
    fig, ax = plt.subplots()
    rects_1 = ax.bar(ind, male_means, width, color=c[0], yerr=male_stds)
    rects_2 = ax.bar(ind + width, female_means, width, color=c[1], yerr=female_stds)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of Candidates')
    ax.set_title('Number of Top-' + str(t) + ' Candidates by gender')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels((fnames_method[0],
                        fnames_method[1],
                        fnames_method[2],
                        fnames_method[3],
                        fnames_method[4],
                        fnames_method[5],
                        fnames_method[6],
                        fnames_method[7]))

    ax.legend((rects_1[0], rects_2[0]), ('Men', 'Women'))

    # def autolabel(rects):
    #     """
    #     Attach a text label above each bar displaying its height
    #     """
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
    #                 '%d' % int(height),
    #                 ha='center', va='bottom')

    # autolabel(rects_1)
    # autolabel(rects_2)

    plt.show()

top_n_results = []
compute_results(top_n_results)

for i, results in enumerate(top_n_results):
    results = top_n_results[i]
    plot(results, ['#4990E2', '#F16E69'], top_n_list[i])