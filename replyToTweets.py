from datetime import time

import config
import tweepy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

user_name = '@twitteru'


# getting the id of the tweet last responded to (prevent duplicate replies)
def get_last_reply_id(user_name):
    tweets = api.user_timeline(screen_name=user_name, count=9, include_rts=False)
    for tweet in tweets:
        if (tweet.in_reply_to_user_id == None):
            return tweet.id


def get_recent_queries(user_name):
    since_id = get_last_reply_id(user_name)
    queries = []
    if since_id:
        replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(user_name), since_id=since_id,
                                tweet_mode='extended').items(5)
        while True:
            try:
                reply = replies.next()
                queries.append(reply.full_text)

            except tweepy.RateLimitError as e:
                exit("Twitter api rate limit reached".format(e))
                time.sleep(60)
                continue

            except tweepy.TweepError as e:
                exit("Tweepy error occured:{}".format(e))
                break

            except StopIteration:
                break

            except Exception as e:
                exit("Failed while fetching replies {}".format(e))
                break

    return queries


def reply_to_queries(user_name):
    queries = get_recent_queries(user_name)
    for query in queries:
        # TODO parse query to get the subject
        print(query)


reply_to_queries(user_name)
