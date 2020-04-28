import pandas as pd
import praw
import json
import csv
import datetime as dt

df = pd.read_csv("post_ids.csv")
use_posts = ('t3_' + df['id'].astype(str)).tolist()

# How many posts left?
print(len(use_posts))

# Read my keys
with open("keys.json") as f:
    keys = json.load(f)

# Initialize reddit API195
reddit = praw.Reddit(client_id=keys['client_id'],
                     client_secret=keys['client_secret'],
                     user_agent=keys['user_agent'])

with open('subreddit_posts_out.csv',"w") as f:
	writer = csv.writer(f, quoting=csv.QUOTE_ALL)
	header = ['id', 'title', 'body', 'num_comments', 'nsfw', 'score', 'timestamp']
	writer.writerow(header)

	i = 0
	counter = 0

	for i in range(0, len(use_posts) + 1, 1000):
		
		end = i + 1000
		if end > len(use_posts):
			end = len(use_posts)
		
		posts = reddit.info(use_posts[i:end])
		for post in posts:

			idx = post.id
			score = post.score

			if score > 0:
				body = post.selftext

				good_body = body != '' and body != '[deleted]' and body != '[removed]'
				if good_body:			
					title = post.title
					
					good_title = title != '' and title != '[deleted]' and title != '[removed]'
					if good_title:
						num_comments = post.num_comments
						nsfw = str(post.over_18)
						timestamp = post.created_utc

						writer.writerow([idx, title, body, num_comments, nsfw, score, timestamp])
						
			counter += 1
			if counter % 1000 == 0:
				print(counter)