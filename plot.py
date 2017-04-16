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
  print ("n : ",n)
  print ("cosine : ", mf_ratio("cosine", 1, n) )
  print ( "jaccard : ", mf_ratio("jaccard", 1, n) )
  print ( "euclidean : ", mf_ratio("euclidean", 1, n) )

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

#def histogram():
  
if __name__ == "__main__":
  #n = 3000
  #get_ratios(n)
  plot ("cosine")
