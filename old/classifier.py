import json
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
import math

stop_words = set(stopwords.words('english'))

jokes = {}
for year in range(2010, 2020):
    jokes[year] = []
    with open(f'reddit_jokes_{year}.json') as json_file:
        year_jokes = json.load(json_file)
            
        year_jokes = [joke for joke in year_jokes if 'selftext' in joke.keys()]
        year_jokes = [joke for joke in year_jokes if joke['title'] not in ['[removed]', '[deleted]', 'removed', 'deleted', '']]
        year_jokes = [joke for joke in year_jokes if joke['selftext'] not in ['[removed]', '[deleted]', 'removed', 'deleted', '']]
        
        for joke in year_jokes:
            joke['year'] = year
            words = joke['title'] + ' ' + joke['selftext']
            # delete these since we absorbed them
            joke.pop('title', None)
            joke.pop('selftext', None)
            
            # we don't need these for now either
            joke.pop('created_utc', None)
            joke.pop('url', None)
            
            # remove punctuation
            words = words.split()
            words = [''.join(ch for ch in word if ch.isalnum()) for word in words]

            # all words to lowercase
            words = [word.lower() for word in words]
            
            words = [word for word in words if word != '']
            # filter out english stopwords
            filtered_words = []
            for w in words: 
                if w not in stop_words: 
                    filtered_words.append(w)
                    
            joke['words'] = filtered_words
            
            
        jokes[year].extend(year_jokes)


# Extract only the score and the words
texts = []
scores = []

years = range(2010, 2020)
for year in years:
    for joke in jokes[year]:
        texts.append(' '.join(joke['words']))
        scores.append(joke['score'])

balanced_x = texts
balanced_y = scores


from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

# This vectorizer breaks text into single words and bi-grams
# and then calculates the TF-IDF representation
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
t1 = datetime.datetime.now()

# the 'fit' builds up the vocabulary from all the reviews
# while the 'transform' step turns each indivdual text into
# a matrix of numbers.
vectors = vectorizer.fit_transform(balanced_x)
print(datetime.datetime.now() - t1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(vectors, balanced_y, test_size=0.33, random_state=42)

from sklearn.svm import LinearSVC

# initialise the SVM classifier
classifier = LinearSVC()

# train the classifier
t1 = datetime.datetime.now()
classifier.fit(X_train, y_train)
print(datetime.datetime.now() - t1)