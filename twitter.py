import tweepy
from secrets import *
from picpurify import *
import re
from externalComms import *


def oauth_login():
    """Authenticate with twitter using OAuth"""
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)    
    return tweepy.API(auth)

def getTwitterInfoFromUser(username):
    twitter =   oauth_login()
    try: 
        userInfo = twitter.get_user(screen_name=username)
        return userInfo.id, userInfo.profile_image_url_https
    except Exception as ex:
        print(ex)
        print("This user does not exist or the twitter api failed") #Manage errors here.
        return -1, -1


 


def  getLastTweetsFromUser(userid, lastTweetIndex): ## Returns tweets from a given user until an index
    
    if str(lastTweetIndex)  == str(404):
        lastTweetIndex = None
    firstLoop = True
    oldest = None
    twitter =   oauth_login()
    alltweets = []
    new_tweets = []

    while len(new_tweets) > 0  or firstLoop:
        firstLoop = False
        try:
            new_tweets = twitter.user_timeline(user_id=userid, count=200, max_id=oldest, since_id=lastTweetIndex, tweet_mode='extended')
        except Exception as ex:
            print(ex)
        alltweets.extend(new_tweets)
        if len(new_tweets) != 0:
            oldest = alltweets[-1].id - 1
    return alltweets


def checkTweet(rules, tweet, daoGroups, user, sendToSlack, slackToken, slackID):
    
    shouldBeInserted = False
    for rule in rules:
        shouldBeInserted = False
        sanitizedTweet = tweet.full_text.encode("latin-1","ignore").decode("latin-1", "strict")

        if rule[0] == 1: ## 1 --> Simple text search
            if textContainingRule(rule, tweet): ##Checks if the keyword is included in the tweet text
                try:
                    shouldBeInserted = True
                    
                except:
                    print("No se pudo insertar")    
        elif rule[0] == 2: ## 2 --> Image Scan
            if 'media' in tweet.entities:
                for media in tweet.extended_entities['media']:
                    print(media['media_url'])
                    result, percentage = picPurifyAPI(media['media_url'], rule[1])
                    if  'KO' in result:
                        shouldBeInserted = True
        elif rule[0] == 3: ## 3 --> Regex search. 
            result = re.search(rule[1], sanitizedTweet)
            if result is not None:
                shouldBeInserted = True

        if shouldBeInserted: 
            daoGroups.insertResult( user[0], rule[3], rule[2],  tweet.id_str, sanitizedTweet)
            if sendToSlack:
                post_message_to_slack(f"<!here>  <https://twitter.com/{user[1]}|{user[1]}>: {sanitizedTweet}  <https://twitter.com/redirect/status/{tweet.id_str}|+>  [{rule[1]}]  ",slackID , slackToken)
            

def textContainingRule(rule, tweet):
    if rule[1].lower() in tweet.full_text.lower():
        return True
    else: 
        return False
