from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import glob
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pymongo import MongoClient
client =MongoClient('localhost',27017)
db =client.twitter
collection = db.abhinandan
senti = SentimentIntensityAnalyzer()

consumer_key = "TufHzi954jfLE7O8YHtK2iFx9"
consumer_secret = "x5QhSUCQfV4QYQd5UfRyVeP8tJSMknEJs07WdOXhTGGh3KdfXx"

access_token = "887731387322650624-UTsVRJN1tnwHuGD8TcZNnKuo0OAf9jj"
access_token_secret = "YWY6AWChWiz6OUaV6ePDyJKcVna03P1vP2nYVautvfIEZ"


class StdOutListener(StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        print(data['text'])
        score =senti.polarity_scores(data['text'])['compound']
        if score>0.1:
            sentiment='positive'
        elif score<-0.1:
            sentiment='negative'
        else:
            sentiment='Neutral'
        data['sentiment'] =sentiment
        collection.insert_one(data)
        
        print('-----------')
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=['#WelcomeHomeAbhinandan'])