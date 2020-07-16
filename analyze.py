from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd

from scrape import get_corpus
from skills import skills

corpus = get_corpus('data scientist')

cv=CountVectorizer(max_df=0.8,stop_words=stop_words, max_features=10000, ngram_range=(2,3))
X=cv.fit_transform(corpus)


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
top_words = get_top_n_words(corpus, n=10)
top_df = pd.DataFrame(top_words)
top_df.columns=["Skill", "Freq"]

top2_words = get_top_n2_words(corpus, n=10)
top2_df = pd.DataFrame(top2_words)
top2_df.columns=["Skill", "Freq"]

top_df = top_df.append(top2_df)
top_df.sort_values('Freq', ascending=False, inplace=True)


print(df.to_json(orient='records'))


## print(top2_df)
##Barplot of most freq Bi-grams
#import seaborn as sns
#sns.set(rc={'figure.figsize':(13,8)})
## plt.title(position + '\n total jobs found: {}'.format(total_jobs))
#plt.title('top skills needed for {}'.format(position))

#h=sns.barplot(x="Skill", y="Freq", data=top_df)
#h.set_xticklabels(h.get_xticklabels(), rotation=45)
#plt.show()