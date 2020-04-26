import pandas as pd
import praw
import json
import csv

df = pd.read_csv("post_ids.csv")
use_posts = df['id'].tolist()

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
	header = ['id', 'title', 'body', 'url', 'distinguished', 'num_comments', 'nsfw', 'score', 'upvote_ratio', 'timestamp']
	writer.writerow(header)

	counter = 0
	for idx in use_posts:
		post = reddit.submission(idx)

		score = post.score
		num_comments = post.num_comments
		title = post.title
		body = post.selftext
		url = post.url
		distinguished = str(post.distinguished)
		nsfw = str(post.over_18)
		upvote_ratio = post.upvote_ratio
		timestamp = post.created_utc

		good_title = title != '' and title != '[deleted]' and title != '[removed]'
		good_body = body != '[deleted]' and body != '[removed]'
		valuable = score > 0 or post.num_comments > 0

		if valuable and good_title and good_body:
				line_stuff = [idx, title, body, url, distinguished, num_comments, nsfw, score, upvote_ratio, timestamp]
				writer.writerow(line_stuff)

		counter += 1
		if counter % 1000 == 0:
				print(counter)
				break
		