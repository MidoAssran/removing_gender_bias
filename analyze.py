from collections import Counter
import csv
import numpy as np
import matplotlib.pyplot as plt

folder = "./data/"
# fnames = ["_cosine_genders_alotaibi.csv",
#           "_euclidean_genders_alotaibi.csv",
#           "_jaccard_genders_alotaibi.csv",
#           "True_euclidean_ranks_g.csv",
#           "False_euclidean_ranks_g.csv",
#           "True_cosine_ranks_g.csv",
#           "False_cosine_ranks_g.csv",
#           "False_jaccard_ranks_g.csv"]

fnames = ["_cosine_genders_alotaibi_II.csv",
          "_euclidean_genders_alotaibi_II.csv",
          "_jaccard_genders_alotaibi_II.csv",
          "True_euclidean_ranks_g_II.csv",
          "False_euclidean_ranks_g_II.csv",
          "True_cosine_ranks_g_II.csv",
          "False_cosine_ranks_g_II.csv",
          "False_jaccard_ranks_g_II.csv"]

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

top_n_list = np.arange(start=100, stop=5000, step=20)
# top_n_list = [100,
#               150, 200,
#               250, 300,
#               350, 400,
#               450, 550,
#               650, 800,
#               850, 900,
#               1000, 1200,
#               1500, 2000,
#               5000]

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

def plot_bar(results, c, t):
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

def get_ratio_per_method(results, n):

    f2m_lst = []
    for method in results:
        male_counts = [job[0] for job in method]
        female_counts = [job[1] for job in method]
        m_avg = np.mean(male_counts)
        f_avg = np.mean(female_counts)
        try:
            f2m = float(f_avg) / float(m_avg)
        except:
            f2m = float(n)
        f2m_lst.append(f2m)

    return f2m_lst

def make_bar(top_n_results):
    for i, results in enumerate(top_n_results):
        results = top_n_results[i]
        plot_bar(results, ['#4990E2', '#F16E69'], top_n_list[i])
def make_roc(top_n_results):

    methods = []
    for i in range(len(fnames_method)):
        methods.append([])

    for i, results in enumerate(top_n_results):
        results = top_n_results[i]
        ratios = get_ratio_per_method(results, top_n_list[i])
        [methods[j].append(ratios[j]) for j in range(len(fnames_method))]

    for i, method in enumerate(methods):
        lbl = fnames_method[i]
        x_axis = top_n_list
        y_axis = method
        plt.plot(x_axis, y_axis, linewidth=1.0,
                 linestyle='-', label=lbl)

    plt.ylabel('Female to Male ratios')
    plt.xlabel('n (top-n threshold)')
    plt.legend()
    plt.show()

def main():
    """ Main method """
    top_n_results = []
    compute_results(top_n_results)
    # make_bar(top_n_results)
    make_roc(top_n_results)

if __name__ == "__main__":
    main()
