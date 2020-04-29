import pandas as pd
import re
import os
import string
from nltk.corpus import stopwords

stop = stopwords.words('english')

qh_pattern = re.compile(r'-')
alnum_pattern = re.compile(r'[^A-Za-z0-9 ]+')

def clean_text(s):
    s = str(s).lower()
    # merge hyphens into the words
    s = qh_pattern.sub('', s)
    # replace with space instead of nothing
    # to cover cases like 'words word.word words'
    s = alnum_pattern.sub(' ', s)
    # remove stop words
    s = ' '.join([word for word in s.split() if word not in stop])
    # to lowercase
    # then remove spaces at the beginning and at the end
    return s.strip()

def clean_scrape(df):
    # merge columns
    df['title'] = df['title'] + ' ' + df['body']
    # count length in chars
    df['body'] = df['title'].apply(lambda x: len(str(x)))
    # then clean
    df['title'] = df['title'].apply(clean_text)
    # make it int instead of float
    df['timestamp'] = df['timestamp'].astype(int)
    # rename the 'title' column
    df.columns = ['id', 'text', 'length', 'num_comments', 'nsfw', 'score', 'timestamp']
    return(df)


# Add the new cleaned results
raw = pd.read_csv("subreddit_posts_out.csv")
clean = clean_scrape(raw)

print("There are now " +  str(len(clean)) + " cleaned posts.")
clean.to_csv("jokes_clean.csv", index=False)