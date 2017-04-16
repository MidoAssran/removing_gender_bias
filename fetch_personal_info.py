from random import randint
import csv
import itertools
import random
import numpy as np

male_keywords = ['He', 'he', 'his', 'man', 'men', 'spokesman', 'himself', 'son',
				'father', 'chairman', 'husband', 'guy', 'boy', 'king', 'Chairman', 'male', 'Man','lions',
				'brothers', 'dad', 'sons', 'kings', 'Men', 'Bulls', 'boyfriend', 'Sir', 'King',
				'businessman', 'Boys', 'grandfather', 'Father', 'uncle', 'Councilman', 'Boy', 'males',
				'guy', 'congressman', 'dad', 'bull', 'businessmen', 'nephew', 'congressmen', 'prostate_cancer',
				'fathers']

female_keywords = ['her', 'she', 'She', 'woman', 'women', 'wife',
					'mother', 'daughter', 'girls', 'girl', 'spokeswoman',
					'female', 'Women', 'herself', 'lady', 'actress', 'mom',
					'girlfriend', 'daughters', 'queen', 'Lady', 'sisters',
					'mothers', 'grandmother', 'Woman', 'cousin', 'Ladies', 'Girls', 
					'mum', 'Girl', 'Queens', 'queen', 'wives', 'widow', 'bride',
					'aunt', 'lesbian', 'chariwoman', 'maiden', 'princess', 'niece',
					'hers', 'filly', 'Actress']

def get_personal_info(gender):
	first_rand_int = randint(0,10)
	second_rand_int = randint(11,20)
	third_rand_int = randint(21,30)
	fourth_rand_int = randint(31,43)
	if(gender == 'male'):
		return [male_keywords[first_rand_int],
		         male_keywords[second_rand_int],
		         male_keywords[third_rand_int],
		         male_keywords[fourth_rand_int]]
	if(gender == 'female'):
		return [female_keywords[first_rand_int],
		         female_keywords[second_rand_int],
		         female_keywords[third_rand_int],
		         female_keywords[fourth_rand_int]]

def get_technical_keywords(technical_keywords):
	return random.sample(technical_keywords,5)

def write_to_csv(fileName, candidates):
	with open(fileName, 'a') as file_handle:
		np.savetxt(file_handle, np.asarray(candidates), delimiter=",", fmt="%s")

technical_keywords = []

with open('job_descriptions.csv', 'rb') as f:
    reader = csv.reader(f)
    technical_keywords = list(reader)
    technical_keywords = get_technical_keywords(list(itertools.chain.from_iterable(technical_keywords)))
    
updated_user_profiles = []
with open('user_profiles.csv', 'rb') as f:
	reader = csv.reader(f)
	vectors = list(reader)
	for vector in vectors:
		updated_user_profiles.append(vector + get_personal_info(vector[7]) + get_technical_keywords(technical_keywords))

write_to_csv('updated_user_profiles.csv', updated_user_profiles)