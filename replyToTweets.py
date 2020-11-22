from datetime import time

import config
import tweepy
import spacy

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

user_name = '@twitteru'

def last_reply_id(user_name):
    """Gets the id of the tweet we most recently responded to (helps to prevent duplicate replies)"""
    tweets = api.user_timeline(screen_name = user_name, count = 10, include_rts = False)
    since_id = None
    for tweet in tweets:
        since_id = tweet.id
        # if (tweet.in_reply_to_user_id == None):
        #     return tweet.id
    return since_id

def recent_queries(user_name):
    """Gets tweets at this account that we haven't replied to yet"""
    since_id = last_reply_id(user_name)
    tweets = []
    if since_id:
        replies = tweepy.Cursor(api.search, q='to:{} filter:replies'.format(user_name), since_id=since_id, tweet_mode='extended').items(10)
        while True:
            try:
                reply = replies.next()
                tweets.append(reply)
            
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

    return tweets


def reply_to_queries(user_name):
    """Sends a tweet to each user who tweeted at this account with a product sentiment"""
    nlp = spacy.load('en')
    def subject_from_query(tweet):
        """Gets the subject of this tweet to analyze"""
        offset = 0
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            for user in tweet.entities['user_mentions']:
                print(user['screen_name'])
                offset += (len(user['screen_name']) + 2)
        doc = nlp(query.full_text[offset:])
        toks = [tok for tok in doc if (tok.dep_ == "nsubj") ]
        toks.sort(key=len, reverse=True)
        return toks
    queries = recent_queries(user_name)
    for query in queries:
        tweet = query.full_text
        product = subject_from_query(tweet)
        if product:
            print(product)
        # pass product to algorithm and get response
        # api.update_status(reply to user with value)


reply_to_queries(user_name)
