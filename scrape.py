import tweepy
import sys
import jsonpickle
import preprocessor as p
import os

consumer_key = "Enter your consumer key here"
consumer_secret = "Enter your consumer secret key here"
access_token = "Enter your access token here"
access_token_secret = "Enter your secret access token here"


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

searchQuery = 'trump'
maxTweets = 900
tweetsPerQry = 100
fName = 'finaldataset2.txt'

sinceId = None

max_id = -1
retweet_filter='-filter:retweets'
tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery+retweet_filter, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery+retweet_filter, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery+retweet_filter, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery+retweet_filter, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                cc={}
                aa = dict(tweet._json)
                aa['text']=aa['text'].replace(',', ' ')
                clean=p.clean(aa['text'])
                user = api.get_user(aa['user']['screen_name'])
                cc['followers_count']=user.followers_count
                cc['friends_count']=user.friends_count
                cc['listed_count']=user.listed_count
                aa['text']=clean
                bb = {'text': aa['text'], 'id': aa['id'], 'recount': aa['retweet_count'], 'favcount': aa['favorite_count'], 'username': aa['user']['screen_name'], 'userfo': cc['followers_count'], 'userfr': cc['friends_count'], 'userl': cc['listed_count']}
                f.write(jsonpickle.encode(bb, unpicklable=False) +
                        '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))