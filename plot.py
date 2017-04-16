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
        data_biased.append( Counter(line1[:n]) )
        data_debiased.append( Counter(line2[:n]) )   

      ratios   = []
      ratios_d = []
      for i in range (len(data_debiased)):
        male     = data_biased[i]["male"]
        male_d   = data_debiased[i]["male"]
        female   = data_biased[i]["female"]
        female_d = data_debiased[i]["female"]

        ratios.append( male/(female+male) )
        ratios_d.append( male_d/(female_d+male_d) )
 
      return ratios, ratios_d

print ( mf_ratio("cosine", 1, 100) )
print ( mf_ratio("jaccard", 1, 100) )
print ( mf_ratio("euclidean", 1, 100) )
