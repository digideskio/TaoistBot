import re
import time
import random
from twitter import *

MAX_MSG_LENGTH  = 140           # characters

CHAPTER_SLEEP   = 30            # seconds
TWEET_SLEEP     = 60 * 60 * 24  # seconds

def read_credentials(file):

    fcred = open('cred.txt', 'r')
    cred = [ k.strip() for k in fcred.readlines() ]
    fcred.close() 
    return cred

def tweet(twitter, msg, sep='.', part=1):

    if len(msg) <= MAX_MSG_LENGTH:
        twitter.statuses.update(status=msg)
        return
    
    lines = msg.split(sep)
    cur = lines[0] + sep + ' '
    for line in lines[1:]:
        line = line.strip()
        if len(line) == 0: continue

        if len(cur) + len(line) <= MAX_MSG_LENGTH - 5:
            cur += line + sep + ' '
        else:
            cur = cur + ' (' + str(part) + ')'
            print cur
            twitter.statuses.update(status=cur)
            part += 1
            if len(line) > MAX_MSG_LENGTH - 5:
                tweet(twitter, line, sep=',', part=part)
                cur = ''
            else:
                cur = line + sep + ' '
            time.sleep(CHAPTER_SLEEP)
    
    if len(cur) > 0:
        cur = cur + ' (' + str(part) + ')'
        print cur
        twitter.statuses.update(status=cur)


# Authorization keys
CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET = read_credentials('cred.txt')

# Read in the text 
ftao = open('taoteching.txt', 'r')
tao = ftao.read()
ftao.close()

chapters = re.split('\d+', tao)[1:]
#print chapters

# Connect up to Twitter
twitter = Twitter(auth=OAuth(
    OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

### MAIN LOOP ###

while(True):
    chapter = random.randint(0, len(chapters)-1)
    tweet(twitter, chapters[chapter].strip())
    time.sleep(TWEET_SLEEP)
