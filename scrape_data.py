from bs4 import BeautifulSoup
from random import randint
import urllib2

base_url = "http://www.indeed.com/resumes/data-science?q=data+science&co=CA"

def scrape_from_all_pages():
	json = {}
	list_to_return = []
	i = 0
	increment_page = '&start=' + str(i)
	while(i<1000000):
		url_to_pass = base_url + increment_page
		increment_page = '&start=' + str(i)
		soup = BeautifulSoup(urllib2.urlopen(base_url+increment_page).read(), 'html.parser')
		results = soup.find_all('li', attrs={'data-tn-component': 'resume-search-result'})
		json = scrape_data(results)
		print json
		i = i + 50
		list_to_return.append(json)
	return list_to_return

def scrape_data(results):
	json_data = {}
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

	    return json_data

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

scrape_from_all_pages()