import requests
import bs4
from bs4 import BeautifulSoup as bs
import pandas as pd

# Importing modules
import pandas as pd
from wordcloud import WordCloud


# Load the regular expression library
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english')) 

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

from multiprocessing import Pool
import multiprocessing


##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))



workers = multiprocessing.cpu_count() - 1

def get_total_jobs(url):
    page = requests.get(url)
    soup=bs(page.text, 'lxml')
    total=soup.find(id='searchCountPages').text
    total = total[total.find('of')+3:total.find('jobs')-1]
    total = total.replace(',','')
    return int(total)

def get_all_links_in_page(url):
    sublist = []
    page = requests.get(url)
    soup=bs(page.text, 'lxml')
    page_list=soup.find('ul', class_='pagination-list')
    try:
        page_len=len(page_list.find_all('li'))
    except:
        print('something went wrong')

    job_listings=soup.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
    for listing in job_listings:
        jk=listing['data-jk']
        job_site=f'https://ca.indeed.com/viewjob?jk={jk}'
        sublist.append(job_site)

    return sublist

def get_all_url_from_job(page):
    start = page*10
    url="https://ca.indeed.com/jobs?q="+position+"&l="+location+"&fromage="+timeline+'&start='+str(start)
    sub_list = get_all_links_in_page(url)
    return sub_list

def scrape(url):
    try:
        response=requests.get(url)
        soup=bs(response.text, 'lxml')
        text=soup.find('div', id='jobDescriptionText').text.strip()
    except:
        print(url)
        print('empty')
    return text


def get_corpus(search_term):

    position=search_term
    

    job_sites={}


    location='Toronto'
    timeline='14'
    start=0

    job_list=[]


    #get first page info
    url="https://ca.indeed.com/jobs?q="+position+"&l="+location+"&fromage="+timeline+'&start='+str(start)

    total_jobs = get_total_jobs(url)
    print(total_jobs)



    p = Pool(workers)
    prelim_job_list = p.map(get_all_url_from_job, list(range(0,int(total_jobs/10))))


    p.terminate()
    p.join()

    flatten = [item for sublist in prelim_job_list for item in sublist]
    job_list = list(set(flatten))

    print(len(job_list))




    p = Pool(workers)
    corpus = p.map(scrape, job_list)


    p.terminate()
    p.join()

    # cleaning the raw text
    corpus = [re.sub('[,\.!?()+]', '', t) for t in corpus]
    corpus = [t.lower() for t in corpus]
    corpus = [t.replace('\n',' ') for t in corpus]

    # text_list = [p_text,p_text]


    # corpus[1]

    for i in range(0,len(corpus)):

        word_tokens = word_tokenize(corpus[i])

        filtered_sentence = [w for w in word_tokens if not w in stop_words] 

        filtered_sentence = [] 

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 
        filtered_sentence_join = ' '.join(filtered_sentence)

        corpus[i] = filtered_sentence_join

    
    
    
    
    
    return corpus