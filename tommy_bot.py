import os
import logging
import re
import random
import praw

from dotenv import load_dotenv
load_dotenv()

LOG_FILE = os.getenv('LOG_FILE')
SUBS = os.getenv('SUBS')
TOMMY_CHANCE = int(os.getenv('CHANCE'))

logging.basicConfig(filename = LOG_FILE,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info('Starting the tommy bot...')

reddit = praw.Reddit('tommybot')
subreddit = reddit.subreddit(SUBS)

pattern = re.compile('[A-Za-z\']+[!|?]+')

for comment in subreddit.stream.comments(skip_existing = True):
  lastWord = comment.body.split(' ')[-1]
  if pattern.match(lastWord) and random.randint(1, 100) <= TOMMY_CHANCE:
    tommyReply = '...' + re.sub('[^A-Za-z\']+', '', lastWord) + re.sub('[^!|?]+', '', lastWord)
    botReply = tommyReply + '''


^Beep ^boop, ^I ^am ^a ^bot. ^Downvote ^me ^if ^I'm ^being ^annoying!'''
    comment.reply(botReply)

    logging.info('Last words of comment: ...' + ' '.join(comment.body.split(' ')[-5:]))

    # log this comment
    with open('comments_replied_to.log', 'a') as f:
      f.write(comment.id + '\n')
      logging.info('Comment id [%s] written to file', comment.id)
