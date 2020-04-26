import pandas as pd
import os

def clean_scrape(df):
    df['body'] = df['body'].str.lower()

    return(df)


# Add the new cleaned results
raw = pd.read_csv("subreddit_posts_out.csv")
grand = clean_scrape(raw)

print("There are now " +  str(len(grand)) + " cleaned posts.")

grand.to_csv("jokes_clean.csv", index=False)