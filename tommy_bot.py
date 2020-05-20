import praw
import re

reddit = praw.Reddit('tommybot')

subreddit = reddit.subreddit('animalcrossing')

for comment in subreddit.stream.comments():
  print (comment.body)
  lastWordRaw = comment.body.split(' ')[-1]
  lastWord = re.sub('[\(\)\.]', '', lastWordRaw)
  if (len(lastWord) > 2 and len(lastWord) < 20):
    print ('...' + re.sub('[^A-Za-z\']+', '', lastWord) + '!')
  else:
    print ('not eligible')
