from bs4 import BeautifulSoup
import copy
from random import randint
import sexmachine.detector as gender
import urllib2
import unicodedata

base_url = "https://www.indeed.com/resumes?q=software&l=victoria"
NUMBER_OF_LISTINGS = 10000 # modify this value to get more data

# d = gender.Detector()

def get_gender():
	# gender = d.get_gender(name)
	# gender_string = unicodedata.normalize('NFKD',gender).encode('ascii','ignore')
	# if gender_string == 'mostly_female' or gender_string == 'andy':
	# 	return 'female'
	# if gender_string == 'mostly_male':
	# 	return 'male'
	# return gender_string
	random_int = randint(0,1)
	if random_int == 0:
		return 'female'
	return 'male'

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

def get_personal_info(candidate_data):
	if(candidate_data['gender'] == 'male'):
		return male_keywords
	if(candidate_data['gender'] == 'female'):
		return female_keywords

def scrape_data(results):
	json_data = {}
	json_list = []
	for x in results:
	    # BSc
	    education = x.find('div', attrs={'class': "education"})
	    json_data['BSc'] = has_bachelors(education)

	    # MSc
	    json_data['MSc'] = has_masters(education)

	    # Tech major
	    experience = x.find_all('div', attrs={'class': "experience"})
	    json_data['tech_major'] = is_in_tech(experience) # tech major - no way to get major - only have access to school

	    # Has worked in tech
	    json_data['has_worked_in_tech'] = is_in_tech(experience) 

	    # Has work experience
	    json_data['work_experience'] = has_work_experience(experience)

	    # Has english skills
	    json_data['english_skills'] = randint(1,3)

	    # Has oracle skill
	    json_data['oracle_skills'] = randint(0,1)

	    # Get name
	    # name = x.find('div', attrs={'class': "app_name"})
	    # json_data['name'] = name
	    # ` name

		# Get gender
	    json_data['gender'] = get_gender()

	    json_data['personal_info'] = get_personal_info(json_data)
	    json_data_to_add = copy.copy(json_data)
	    json_list.append(json_data_to_add)
	    # print '------------'
	    # print x
	    # print json_data
	    # print '------------'
	    json_data.clear()
	return json_list

def scrape_from_all_pages():
	json = {}
	list_to_return = []
	i = 0
	increment_page = '&co=CA&start=' + str(i)
	while(i<NUMBER_OF_LISTINGS):
		increment_page = '&co=CA&start=' + str(i)
		url_to_pass = base_url + increment_page
		try:
			soup = BeautifulSoup(urllib2.urlopen(url_to_pass).read(), 'html.parser')
		except:
			return list_to_return
		results = soup.find_all('li', attrs={'data-tn-component': 'resume-search-result'})
		list_json = scrape_data(results)
		i = i + 50
		list_to_return.append(list_json)
	return list_to_return

def has_bachelors(education):
	if education is None:
		return 0
	bachelor_keywords = ['bsc', 'bachelors', 'bachelor', 'undergraduate']
	for keyword in bachelor_keywords:
		if keyword in str(education).lower():
			return 1
	return 0

def has_masters(education):
	if education is None:
		return 0
	masters_keywords = ['msc', 'masters', 'master', 'graduate']
	for keyword in masters_keywords:
		if keyword in str(education).lower():
			return 1
	return 0

def is_in_tech(experience):
	if experience is None:
		return 0
	tech_keywords = ['developer', 'programmer', 'software', 'software egineering', 'computer programming', 'IT', 'computer', 'programming']
	for i, exp in enumerate(experience):
	    if str(exp).lower() in tech_keywords:
			return 1
	return 0

def has_work_experience(experience):
	# we assume on average a candidate works 3 jobs in 4 years
	if experience is None:
		return 0
	count = 0
	for i, exp in enumerate(experience):
		count+=1
	if count >= 3:
		return 1
	else:
		return 0

#scrape_from_all_pages()