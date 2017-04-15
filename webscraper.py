from bs4 import BeautifulSoup
#import urllib.request as urllib2
import urllib2
import re
from time import sleep 
from collections import Counter 
from nltk.corpus import stopwords 
import pandas as pd

def text_cleaner(website):
    try:
        site = urllib2.urlopen(website).read()
    except: 
        return
    soup_obj = BeautifulSoup(site)

    if len(soup_obj) == 0:
        soup_obj = BeautifulSoup(site, 'html5lib')

    for script in soup_obj(["script", "style"]):
        script.extract() 

    text = soup_obj.get_text()
    lines = (line.strip() for line in text.splitlines()) 
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) 
    text = ''.join(chunk for chunk in chunks if chunk).encode('utf-8') 
    
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore')
    except: 
        return
    text = re.sub('[^a-zA-Z+3]',' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text) 
    text = text.lower().split()  
    
    stop_words = set(stopwords.words("english"))
    text = [w for w in text if not w in stop_words]
    text = list(set(text)) 

    return text

def skills_info(city = None, state = None):
    final_job = 'data+scientist' 
    if city is not None:
        final_city = city.split() 
        final_city = '+'.join(word for word in final_city)
        final_site_list = ['http://www.indeed.com/jobs?q=%22', final_job, '%22&l=', final_city,
                   '%2C+', state] 
    else:
        final_site_list = ['http://www.indeed.com/jobs?q="', final_job, '"']

    final_site = ''.join(final_site_list) 
    base_url = 'http://www.indeed.com'
    try:
        html = urllib2.urlopen(final_site).read()
    except:
        'That city/state combination did not have any jobs. Exiting . . .'
        return
    soup = BeautifulSoup(html)

    num_jobs_area = soup.find(id = 'searchCount').string.encode('utf-8')
    job_numbers = re.findall('\d+', num_jobs_area)


    if len(job_numbers) > 3:
        total_num_jobs = (int(job_numbers[2])*1000) + int(job_numbers[3])
    else:
        total_num_jobs = int(job_numbers[2]) 

    city_title = city
    if city is None:
        city_title = 'Nationwide'
    
    print ('There were', total_num_jobs, 'jobs found,', city_title)

    num_pages = total_num_jobs/10
    job_descriptions = []

    for i in xrange(1,num_pages+1):
        print ('Getting page', i)
        start_num = str(i*10)
        current_page = ''.join([final_site, '&start=', start_num])
        html_page = urllib2.urlopen(current_page).read()
        
        page_obj = BeautifulSoup(html_page)
        job_link_area = page_obj.find(id = 'resultsCol')
        
        job_URLS = [base_url + link.get('href') for link in job_link_area.find_all('a')]
        job_URLS = filter(lambda x:'clk' in x, job_URLS)
    
        for j in xrange(0,len(job_URLS)):
            final_description = text_cleaner(job_URLS[j])
            if final_description:
                job_descriptions.append(final_description)
            sleep(1)
    print ('Done with collecting the job postings!')
    print ('There were', len(job_descriptions), 'jobs successfully found.')


    doc_frequency = Counter() 
    [doc_frequency.update(item) for item in job_descriptions] 

    prog_lang_dict = Counter({'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                   'Ruby':doc_frequency['ruby'],
                  'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                  'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala']})
                  
    analysis_tool_dict = Counter({'Excel':doc_frequency['excel'], 'Tableau':doc_frequency['tableau'],
                      'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                      'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3']})  

    hadoop_dict = Counter({'Hadoop':doc_frequency['hadoop'], 'MapReduce':doc_frequency['mapreduce'],
               'Spark':doc_frequency['spark'], 'Pig':doc_frequency['pig'],
               'Hive':doc_frequency['hive'], 'Shark':doc_frequency['shark'],
               'Oozie':doc_frequency['oozie'], 'ZooKeeper':doc_frequency['zookeeper'],
               'Flume':doc_frequency['flume'], 'Mahout':doc_frequency['mahout']})
               
    database_dict = Counter({'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                 'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                 'MongoDB':doc_frequency['mongodb']})
                 
    overall_total_skills = prog_lang_dict + analysis_tool_dict + hadoop_dict + database_dict 
    final_frame = pd.DataFrame(overall_total_skills.items(), columns = ['Term', 'NumPostings'])
    final_frame.NumPostings = (final_frame.NumPostings)*100/len(job_descriptions)
    final_frame.sort(columns = 'NumPostings', ascending = False, inplace = True)

    
    final_plot = final_frame.plot(x = 'Term', kind = 'bar', legend = None, 
                title = 'Percentage of Data Scientist Job Ads with a Key Skill, ' + city_title)
    
    final_plot.set_ylabel('Percentage Appearing in Job Ads')
    fig = final_plot.get_figure() 
    
    return fig, final_frame

webpage = "https://www.indeed.com/rc/clk?jk=52aa63c90ef60f59&fccid=eca8608f9f563439"
wp = "https://www.indeed.com/rc/clk?jk=50c440fc38558f6f&fccid=7a3824693ee1074b"
#sample = text_cleaner(webpage)
sample = text_cleaner(wp)
seattle_info = skills_info(city = 'San Francisco', state = 'CA')
print (seattle_info)
# "MSc"
# "BSc"
# "tech_major" --> 1/0
# "has_worked_in_tech" --> 1/0
# "work_experience" 4+ years
# "english_skills" 1,2,3
# "oracle_skills" 1/0


