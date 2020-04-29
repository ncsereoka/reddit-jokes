# Analysis of r/Jokes

## Introduction

First and foremost, why [r/Jokes](https://reddit.com/r/jokes)? It struck me while browsing Reddit that this _should_ be a goldmine for text analysis. Thousands of posts, each scored and judged by objective redditors.

There must be an API to download all this data. Two searches and I find [PRAW: The Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/). OK, let's set this up - look at some tutorials, use your Reddit to account create an API key to be used in your script...

Now, create a basic script to fetch me the newest 100 posts. Sweet. I need more, though. I need to cycle through id's? How do I do that? Read some more posts. Yeah, it's not going to work like this.

[Pushshift](https://pushshift.io/) gets thrown around, which should solve my problems, as it crawls and archives most of Reddit. This API allows me to cycle through posts using timestamps as basic url parameters and so I can download quite a lot of posts. Community, please keep Pushshift running.

I manage to download around 360 000 posts. While analyzing the data, I realize that it isn't quite what I want - as I've read from several sites, Pushshift actually saves the state of the post at the time of crawling. I've found that some posts with a great number of comments got only a score of 1 when they actually have 32k. This makes my analysis inaccurate. I need to go back to PRAW as it will get me real data.

Here comes a lot of frustration. But then I find [this article](https://dvc.org/blog/a-public-reddit-dataset) from Elle O'Brien and DVC. Great stuff, now we're talking.

## Step 1: Get the data

Ellen gives us the [scripts](https://github.com/iterative/aita_dataset) from her process.

One thing to note: I suppose she used this approach because, as many others have realized, parsing with PRAW takes a lot of time. Pushshift makes a great job in simplifying the process. Fetch the id's, and then - since we want fresh data - use PRAW for the actual stuff.

I tweaked the second script to use r/Jokes and I added some other attributes for the posts - in particular, **upvote_ratio**. Let's start the script. It takes a lot of time. Almost two minutes for 1000 posts and it started to grow, but seemed to plateau at 4 minutes for 1000 posts.

This is not right. Did she let the script run that much time? Is it supposed to take this long?. I give in and let it run for the night. Waking up, I see that the process got interrupted at 72 000 due to a network error. It can't be right.

I thought that calling `reddit.submission` was the culprit. Instead, I sought to use `reddit.info` which would allow me to query 100 submissions in one go by giving it a list of id's. The speed is still bad.

I start to debug, timing all the instructions from the script. I found that `upvote_ratio = post.upvote_ratio` took almost **400ms** as opposed to the other operations, such as the `writer` call which rarely exceeded **1ms**. After a search, I found that this makes an extra API call and that results in the overhead. Probably, it would've given an extra edge in analysis, but I had to get rid of the attribute. Now, a speed of 1000 posts in approximately 10 seconds, running it for about 3.5 hours. Out of **1.06 million** post id's from Pushshift, only **447 000** submissions make it through the checks (non-empty, non-deleted title or body). I didn't want my dataset to look like it did last time - almost 75% of posts under a score of 10.

Conclusion: Double check your scraping scripts - might save you and external APIs loads of time and bandwidth.

## Step 2: Data cleanup

Why not do the cleanup along the way in the scraping script? I think it adds a lot of overhead. Get the data first, then play with it after. Don't sabotage your script by making it take more time then necessary in between requests.

Merge the `title` and `body` columns since a lot of jokes use the title as the setup for the punchline. Count length, everything to lowercase and keep only alphanumeric characters. Remove stopwords.

## Step 3: Broad look
