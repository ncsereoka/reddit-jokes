import requests
import json
import threading
import time

size = 1000
urlFormatString = f'https://api.pushshift.io/reddit/submission/search/?subreddit=jokes&after=%s&before=%s&size={size}'

def get_extract_from_post(post):
	required_fields = ['created_utc', 'gilded', 'num_comments', 'over_18', 'score', 'selftext', 'spoiler', 'title', 'url']
	return {key:value for key, value in post.items() if key in required_fields}

def get_extracts_from_response(res):
	data = res.json()['data']
	return [get_extract_from_post(post) for post in data]

def write_joke_file_for_year(year):
	jokes = []

	# get the jokes from the year
	for month in range(1, 13):
		prefix = '%d-%02d' % (year, month)
		print(f'Retrieving {prefix}...')

		# take {size} from each week
		for day in range(1, 29, 4):
			after = '%s-%02d' % (prefix, day)
			before = '%s-%02d' % (prefix, day + 3)
			url = urlFormatString % (after, before)
			response = requests.get(url)
			jokes.extend(get_extracts_from_response(response))
			time.sleep(1)

	# dump jokes of the year to a json
	filename = f'reddit_jokes_{year}.json'
	with open(filename, 'w') as fp:
		json.dump(jokes, fp)

for year in range(2019, 2020):
	write_joke_file_for_year(year)
	
