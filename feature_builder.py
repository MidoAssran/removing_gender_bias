from scrape_data import scrape_from_all_pages
import numpy as np

def has_masters(resume_data):
	# masters_keyword = 'MSc'
	# if masters_keyword not in resume_data:
	# 	return 0
	# return 1
	return resume_data["MSc"]

def has_bachelors(resume_data):
	# bachelors_keyword = 'BSc'
	# if bachelors_keyword not in resume_data:
	# 	return 0
	# return 1
	if resume_data["MSc"] == 0:
		return 1 # since a bachelors is required in the paper
	return resume_data["BSc"]

def is_in_tech_major(resume_data):
	# tech_keywords = ['Software Engineering', 'Computer Programming', 'IT']
	# for tech_keyword in tech_keywords:
	# 	if tech_keyword in resume_data:
	# 		return 1
	# 	else:
	# 		continue
	# return 0
	return resume_data["tech_major"]

def has_worked_in_tech(resume_data):
	return resume_data["has_worked_in_tech"] 

def has_work_experience(resume_data):
	return resume_data["work_experience"]

def has_english_skills(resume_data):
	return resume_data["english_skills"]

def has_oracle_skills(resume_data):
	return resume_data['oracle_skills']

# def get_name(resume_data):
# 	return resume_data['name']

def get_gender(resume_data):
	return resume_data['gender']

def get_personal_info(resume_data):
	return resume_data['personal_info']


def construct_candidate_skills(resume_data):
	masters = has_masters(resume_data)
	bachelors = has_bachelors(resume_data)
	tech_major = is_in_tech_major(resume_data)
	worked_in_tech = has_worked_in_tech(resume_data)
	work_experience = has_work_experience(resume_data)
	english_skills = has_english_skills(resume_data)
	oracle_skills = has_oracle_skills(resume_data)
	candidate_info = [masters,bachelors, tech_major, worked_in_tech, work_experience,english_skills, oracle_skills, get_gender(resume_data)]
	return candidate_info + get_personal_info(resume_data)

candidates = scrape_from_all_pages()
candidates_list = []
for candidate in candidates:	
	vector = construct_candidate_skills(candidate)
	candidates_list.append(vector)

def write_to_csv(fileName, candidates):
	np.savetxt(fileName, np.asarray(candidates), delimiter=",", fmt="%s")

write_to_csv('user_profiles.csv', candidates_list)
# TODO: Add "load_alotaibi_users, load_alotaibi_jobs"