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
        twitter.statuses.update(status=msg)
        print verse
        return part+1
   
    chunks = verse.split(sep)
    #print chunks
    buf = ''
    for i, chunk in enumerate(chunks):
        if len(chunk) == 0: continue
        chunk = chunk.strip()
        if i < len(chunks)-1: chunk += sep
        
        if len(buf) + len(chunk) <= MAX_MSG_LENGTH - 5:
            buf += chunk
            continue

        if len(buf) > 0:
            buf += ' ({0})'.format(part)
            print buf
            buf = ''
            part += 1
        
        if len(chunk) > MAX_MSG_LENGTH - 5:
            new_sep = ', ' if sep == '. ' else '; '
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
    #chapter = 49
    try:
        tweet_chapter(twitter, chapters[chapter].strip())
    except Exception as e:
        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Error: " + e.strerror
        twitter.statuses.update(status="Woops, something went wrong.")
        #ferr = open('err.log', 'w+')
        #ferr.write(
    time.sleep(TWEET_SLEEP)
