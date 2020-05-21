import praw
import re
import logging
import os

from dotenv import load_dotenv
load_dotenv()

LOG_FILE = os.getenv('LOG_FILE')
SUBS = os.getenv('SUBS')

logging.basicConfig(filename = LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info('Starting the tommy bot...')

# Get comments we already replied to
with open('comments_replied_to.log', 'r') as f:
  comments_replied_to = f.read()
  comments_replied_to = comments_replied_to.split('\n')
  comments_replied_to = list(filter(None, comments_replied_to))
  logging.info('Got comments we already replied to')

reddit = praw.Reddit('tommybot')
subreddit = reddit.subreddit(SUBS)

pattern = re.compile('[A-Za-z\']+[!|?]+')

for comment in subreddit.stream.comments(skip_existing = True):
  lastWord = comment.body.split(' ')[-1]
  if pattern.match(lastWord) and comment.id not in comments_replied_to:
    print (comment.body)
    tommyReply = '...' + re.sub('[^A-Za-z\']+', '', lastWord) + re.sub('[^!|?]+', '', lastWord)
    print (tommyReply)
    # comment.reply(tommyReply)

    # log this comment
    with open('comments_replied_to.log', 'a') as f:
      f.write(comment.id + '\n')
      logging.info('Comment id [%s] written to file', comment.id)
