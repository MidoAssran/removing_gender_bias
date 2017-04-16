import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import Counter

def mf_ratio(method,gender,n):
  g = ("","_g")[gender]
  f1 = "data/False_"+method+"_ranks"+g+".csv"
  f2 = "data/True_"+method+"_ranks"+g+".csv"

  with open(f1, 'r') as csv1,  open(f2,'r') as csv2:
      res1 = csv.reader(csv1)
      res2 = csv.reader(csv2) 
      
      data_biased   = []
      data_debiased = []

      for line1,line2 in zip(res1,res2):
        data_biased.append( Counter(line1) )
        data_debiased.append( Counter(line2) )

      ratios   = []
      ratios_d = []

      for i in range (len(data_debiased)):
        male     = data_biased[i]["male"]
        male_d   = data_debiased[i]["male"]
        female   = data_biased[i]["female"]
        female_d = data_debiased[i]["female"]

        ratios.append( male/(female+male) )
        ratios_d.append( male_d/(female_d+male_d) )
 
      #print (np.std(ratios))
      #print (np.std(ratios_d))
      #print (ratios, ratios_d)
      return np.average(ratios), np.average(ratios_d)

def get_ratios(n):
  #print ("n : ",n)
  cos = ("cosine : ", mf_ratio("cosine", 1, n) )
  jac = ( "jaccard : ", mf_ratio("jaccard", 1, n) )
  euc = ( "euclidean : ", mf_ratio("euclidean", 1, n) )
  #print (cos)
  #print (jac)
  #print (euc)
  return cos, jac, euc
  

def plot(method):
  n = np.arange(1,101)*100
  r = [mf_ratio(method, 1, j) for j in n]

  biased = np.array([x[0] for x in r])*100
  debiased = np.array([x[1] for x in r])*100

  biased_female = np.array([ 100-x for x in biased ])
  debiased_female = np.array([100-x for x in debiased ])
  print (r)
  
  m_b, = plt.plot(n,biased, 'b--')
  m_d, = plt.plot(n,debiased, 'c--')
  f_b, = plt.plot(n,biased_female, 'r--')
  f_d, = plt.plot(n,debiased_female, 'm--')

  plt.legend([m_b, m_d, f_b, f_d],['Male', 'Male Debiased', 'Female', 'Female Debiased'], loc="upper right", ncol=1, fontsize=8)
  plt.title('Gender Percentage of the Top n Selected Candidates Using Cosine')
  plt.ylabel('Percentage')
  plt.xlabel('n')
  plt.show()

def barchart():
  cosine, jaccard, euclidean = get_ratios(800)
  print (cosine[1][0])
  print (jaccard[1])

  male = (cosine[1][0], jaccard[1][0], euclidean[1][0], cosine[1][1], jaccard[1][1], euclidean[1][1])
  female = (1-cosine[1][0], 1-jaccard[1][0], 1-euclidean[1][0],1-cosine[1][1], 1-jaccard[1][1], 1-euclidean[1][1])

  n = [1,2,3,4,5,6]
  np1 = [0.825,1.825,2.825,3.825,4.825,5.825]
  np2 = [1.175,2.175,3.175,4.175,5.175, 6.175]

  width = 0.35
  p1 = plt.bar(np1,male, width, color='#7a9eea')
  p2 = plt.bar(np2,female, width, color='#d62728')

  plt.ylabel('Percentage')
  plt.title('Scores by Method by Gender')
  plt.xticks(n, ('CosB', 'JaccB', 'EucliB', 'CosDB', 'JaccDB', 'EucliDB'))
  #plt.legend((male[0], female[0]), ('Men', 'Women'))
  plt.show()

   

  
if __name__ == "__main__":
  #n = 3000
  #get_ratios(n)
  #plot ("cosine")
  barchart()
