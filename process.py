import plotly
import plotly.graph_objs as go
import tweepy
import jsonpickle
from tweepy import OAuthHandler
from textblob import TextBlob
import json
class TwitterProcessor(object):

 def __init__(self):

        consumer_key = 'Enter your consumer key here'
        consumer_secret = 'Enter your consumer secret here'
        access_token = 'enter your access token here'
        access_token_secret = 'enter your secret access token here'

        try:

            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")

 def get_weight(self,name):
     user = self.api.get_user(name)
     sum = (0.25)*user.friends_count + (2.5)* user.followers_count + (0.25)*user.listed_count
     return sum



 def get_scoredtweets(self,tweets):
     ftweets=[]
     for tweet in tweets:
         weighted_tweets={}
         weighted_tweets['username']=tweet['username']
         sum=(0.6)*tweet['userfo']+(0.16)*tweet['userfr']+(0.16)*tweet['userl']
         sum1=(0.10)*tweet['favcount']+(0.90)*tweet['recount']
         weighted_tweets['score']=((0.25)*sum+(0.75)*sum1)/1000
         weighted_tweets['text']=tweet['text']
         weighted_tweets['sentiment']=self.get_tweet_sentiment(tweet['text'])
         if(weighted_tweets['sentiment']=='negative'):
             weighted_tweets['score']=(-1)*weighted_tweets['score']
         ftweets.append(weighted_tweets)
     return ftweets


 def get_tweets(self):
     file = open('finaldataset1.txt', 'r')
     tweetdata = []
     text = file.readlines()
     for i in text:
         tweetdata.append(json.loads(i))
     return tweetdata


 def get_tweet_sentiment(self, tweet):
     analysis = TextBlob(tweet)
     if analysis.sentiment.polarity > 0:
         return 'positive'
     elif analysis.sentiment.polarity == 0:
         return 'neutral'
     else:
         return 'negative'



def main():

    api = TwitterProcessor()
    pscore=0
    fname='positive.txt'
    fname1='negative.txt'
    fname2='neutral.txt'
    max1=0
    nscore=0
    nescore=0
    tweets = api.get_tweets()
    cumulative_score = 0
    max=0
    min=1000
    ftweets = api.get_scoredtweets(tweets)

    for t in ftweets:
        cumulative_score=cumulative_score+t['score']
        if(t['score']>max):
            max=t['score']
            m=t['text']
            u=t['username']
        if(t['score']<min):
            min=t['score']
            l=t['text']
            u1=t['username']

    print('Cumulative score:',cumulative_score,'\n')
    print('Highiest impact positive tweet:',m,'by ',u,'\n')
    print('Highiest impact negative tweet is:',l,' by ',u1,'\n')

    ptweets = [tweet for tweet in ftweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)),'\n')

    for p in ptweets:
        pscore=pscore+p['score']

    ntweets = [tweet for tweet in ftweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)),'\n')

    for n in ntweets:
        nscore=nscore+(-1)*n['score']

    print("Neutral tweets percentage: {} % \
    ".format(100 * (len(ftweets) - len(ntweets) - len(ptweets)) / len(ftweets)),'\n')


    nep=100 * (len(ftweets) - len(ntweets) - len(ptweets)) / len(ftweets)
    np=100 * len(ntweets) / len(tweets)
    pp=100 * len(ptweets) / len(tweets)
    netweets = [tweet for tweet in ftweets if tweet['sentiment'] == 'neutral']

    for n in netweets:
        nescore=nescore+n['score']
        if(max1<n['score']):
            max1=n['score']
            t1=n['text']
            u3=n['username']
    print("Highiest impact neutral tweet is",t1,' by ',u3,'\n')
    ippt=100 * pscore/(pscore+nscore+nescore)
    ipnt=100 * nscore/(pscore+nscore+nescore)
    ipnet=100 * nescore / (pscore + nscore + nescore)
    print("Impact percentage of positive tweets: {} %".format(100 * pscore/(pscore+nscore+nescore)),'\n')
    print("Impact percentage of negative tweets: {} %".format(100 * nscore / (pscore + nscore + nescore)),'\n')
    print("Impact percentage of neutral tweets: {} %".format(100 * nescore / (pscore + nscore + nescore)),'\n')

    newlistp = sorted(ptweets, key=lambda x: x['score'], reverse=True)
    newlistn = sorted(ntweets, key=lambda x: x['score'], reverse=False)
    newlistne = sorted(netweets, key=lambda x: x['score'], reverse=True)
    with open(fname, 'w') as f:
     for k in newlistp:
         bb = {'text': k['text'], 'username': k['username'], 'score': k['score']}
         f.write(jsonpickle.encode(bb, unpicklable=False) +
                 '\n\n')

     with open(fname1, 'w') as f:
      for k in newlistn:
         bb = {'text': k['text'], 'username': k['username'], 'score': k['score']}
         f.write(jsonpickle.encode(bb, unpicklable=False) +
                         '\n\n')

     with open(fname2, 'w') as f:
      for k in newlistp:
         bb = {'text': k['text'], 'username': k['username'], 'score': k['score']}
         f.write(jsonpickle.encode(bb, unpicklable=False) +
                         '\n\n')

    correctness=(ippt-ipnt)/(pp-np)
    difference = ((ippt-pp)+(ipnt-np)+(ipnet-nep))/3
    print('mean difference value is',difference)
    print('correctenss :',correctness,'\n')
    if(correctness<0):
     if((ippt-ipnt)<0):
         print('sentiment analysis is not right about the impact because: \n')
         print('Opinions of commoners and influential people are clashing ,Many influential people are not liking Modi government')
     elif((pp-np)<0):
         print('sentiment analysis is not right about the impact because:\n')
         print('Opinions of commoners and influential people are clashing ,Many common people are not liking Modi governement')
    if (correctness > 0):
        if (((ippt - ipnt) > 0)and((pp-np)>0)):
            print(
                'Opinions of commoners and influential people are same ,they both are liking Modi government')
        else:
            print('Opinions of commoners and influential people are same ,they both are not liking Modi governement')

    labels = ['Positive', 'Negative', 'Neutral']
    values = [pp,np,nep]

    trace = go.Pie(labels=labels, values=values)

    plotly.offline.plot([trace], filename='percentage_pie_chart.html')

    labels = ['Positive', 'Negative', 'Neutral']
    values = [ippt,ipnt,ipnet]

    trace = go.Pie(labels=labels, values=values)

    plotly.offline.plot([trace], filename='impact_percentage_pie_chart.html')
if __name__ == "__main__":
    main()
