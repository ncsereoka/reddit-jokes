import pandas as pd
import re
import os
import string

qh_pattern = re.compile(r'-|\'')
alnum_pattern = re.compile(r'[^A-Za-z0-9 ]+')
space_pattern = re.compile('\s{2,}')

def clean_text(s):
    s = str(s)
    # merge single quotes and hypens into the words
    s = qh_pattern.sub('', s)
    # replace with space instead of nothing
    # to cover cases like 'words word.word words'
    s = alnum_pattern.sub(' ', s)
    # remove excess whitespace
    s = space_pattern.sub(' ', s)
    # to lowercase
    # then remove spaces at the beginning and at the end
    return s.lower().strip()
    

def clean_scrape(df):
    # merge columns
    df['title'] = df['title'] + ' ' + df['body']
    # then clean
    df['title'] = df['title'].apply(clean_text)
    # drop the body
    del df['body']
    # make it int instead of float
    df['timestamp'] = df['timestamp'].astype(int)
    # rename the 'title' column
    df.columns = ['id', 'text', 'num_comments', 'nsfw', 'score', 'timestamp']
    return(df)


# Add the new cleaned results
raw = pd.read_csv("subreddit_posts_out.csv")
clean = clean_scrape(raw)

print("There are now " +  str(len(clean)) + " cleaned posts.")
clean.to_csv("jokes_clean.csv", index=False)
