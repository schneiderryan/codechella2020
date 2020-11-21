import config
import tweepy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)


def lookupTweets(keyword):

    class MyStreamListener(tweepy.StreamListener):
        def on_status(self, status):

            tweet_text = status.text

            return tweet_text

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=[keyword])


# lookup tweets by keyword, returns text of tweet
lookupTweets("Twitter")
