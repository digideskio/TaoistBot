import re
import time
import random
from twitter import *

MAX_MSG_LENGTH  = 140           # characters

CHAPTER_SLEEP   = 60 * 30       # seconds
TWEET_SLEEP     = 60 * 60 * 24  # seconds

def read_credentials(file):

    fcred = open('cred.txt', 'r')
    cred = [ k.strip() for k in fcred.readlines() ]
    fcred.close() 
    return cred

def tweet_chapter(twitter, chapter):
    
    verses = chapter.split('\n')
    for verse in verses:
        print
        tweet(twitter, verse.strip())

def tweet(twitter, verse, sep='. ', part=1):
    
    if len(verse) <= MAX_MSG_LENGTH:
        twitter.statuses.update(status=verse)
        print verse
        time.sleep(CHAPTER_SLEEP)
        return part+1
   
    chunks = verse.split(sep)
    #chunks = re.split(sep, verse)
    #print chunks
    buf = ''
    for i, chunk in enumerate(chunks):
        if len(chunk) == 0: continue
        chunk = chunk.strip()
        if i < len(chunks)-1: chunk += sep
        
        if len(buf) + len(chunk) <= MAX_MSG_LENGTH - 5:
            buf += chunk
            continue

        if len(buf) > 0: # stuff in buf, tweet and flush
            buf += ' ({0})'.format(part)
            #print buf
            tweet(twitter, buf, sep=sep, part=part)
            buf = ''
            part += 1
        
        if len(chunk) > MAX_MSG_LENGTH - 5:
            #new_sep = ', ' if sep == '. ' else '; '
            if   sep == '. ': new_sep = ', '
            elif sep == ', ': new_sep = '; '
            elif sep == '; ': new_sep = '? '
            part = tweet(twitter, chunk, sep=new_sep, part=part)
        else:
            buf = chunk

    if len(buf) > 0:
        buf += ' ({0})'.format(part)
        print buf
        part += 1

    return part
        


# Authorization keys
CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET = read_credentials('cred.txt')

# Read in the text. The text format is as follows
#   <chapter n>
#   <verse 1>
#   <verse 2>
#   ...
#   <verse n>
#
#   <chapter n+1>
#   ... 
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
    #chapter = 12
    tweet_chapter(twitter, chapters[chapter].strip())
    time.sleep(TWEET_SLEEP)
