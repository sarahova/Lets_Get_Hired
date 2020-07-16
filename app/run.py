
import requests
import bs4
from bs4 import BeautifulSoup as bs
import pandas as pd
# import time
from tqdm import tqdm_notebook

# Importing modules
import pandas as pd
# from wordcloud import WordCloud
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

from skills import skills





##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))

##Creating a list of custom stopwords
# new_words = ["using", "show", "result", "large", "also", "iv", "one", "two", "new", "previously", "shown", 'business', 'client', 'need']
# stop_words = stop_words.union(new_words)


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



def get_all_url_from_job(page, position, location, timeline):
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
        text=''  
        print(url)
        print('empty')
    return text








# from PIL import Image
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# import matplotlib.pyplot as plt
# % matplotlib inline


# wordcloud = WordCloud(width=800, height=400).generate(str(corpus))
# plt.figure( figsize=(20,10), facecolor='k')
# plt.imshow(wordcloud)
# plt.show()


from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd



#Most frequently occuring words
def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items() if word in skills]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq[:n]
#Most frequently occuring Bi-grams
def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),  
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec1.vocabulary_.items() if word in skills]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

#Convert most freq words to dataframe for plotting bar plot

# #Barplot of most freq Bi-grams
# import seaborn as sns
# sns.set(rc={'figure.figsize':(13,8)})
# # plt.title(position + '\n total jobs found: {}'.format(total_jobs))
# plt.title('top skills needed for {}'.format(position))

# h=sns.barplot(x="Skill", y="Freq", data=top_df)
# h.set_xticklabels(h.get_xticklabels(), rotation=45)
# plt.show()





def run_all(string):

    multi=False

    position=string

    job_sites={}


    location='Toronto'
    timeline='14'
    start=0

    job_list=[]
 


    #get first page info
    url="https://ca.indeed.com/jobs?q="+position+"&l="+location+"&fromage="+timeline+'&start='+str(start)

    total_jobs = get_total_jobs(url)

    if multi:
        # multiprocessing
        p = Pool(workers)
        prelim_job_list = p.map(get_all_url_from_job, list(range(0,int(total_jobs/10))))
        p.terminate()
        p.join()

    else:
        #single_process
        prelim_job_list = []
        for p in list(range(0,int(total_jobs/10))):
            prelim_job_list.append(get_all_url_from_job(p, position, location, timeline))

    flatten = [item for sublist in prelim_job_list for item in sublist]
    job_list = list(set(flatten))


    if multi:
        p = Pool(workers)
        corpus = p.map(scrape, job_list)
        p.terminate()
        p.join()

    else:
        corpus = []
        for p in job_list:
            corpus.append(scrape(p))


    # cleaning the raw text
    corpus = [re.sub('[,\.!?()+]', '', t) for t in corpus]
    corpus = [t.lower() for t in corpus]
    corpus = [t.replace('\n',' ') for t in corpus]

    # text_list = [p_text,p_text]


    for i in range(0,len(corpus)):

        word_tokens = word_tokenize(corpus[i])

        filtered_sentence = [w for w in word_tokens if not w in stop_words] 

        filtered_sentence = [] 

        for w in word_tokens: 
            if w not in stop_words: 
                filtered_sentence.append(w) 
        filtered_sentence_join = ' '.join(filtered_sentence)

        corpus[i] = filtered_sentence_join


    cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(2,3))
    X=cv.fit_transform(corpus)

    top_words = get_top_n_words(corpus, n=10)
    top_df = pd.DataFrame(top_words)
    top_df.columns=["label", "y"]

    top2_words = get_top_n2_words(corpus, n=10)
    top2_df = pd.DataFrame(top2_words)
    top2_df.columns=["label", "y"]

    top_df = top_df.append(top2_df)
    top_df.sort_values('y', ascending=True, inplace=True)
    print(top_df.to_json(orient='records'))
    return  top_df.to_dict(orient='records'), position
    

if __name__ == '__main__':
    run_all('data scientist')