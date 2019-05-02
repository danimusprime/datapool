from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Cursor
import psycopg2 as pg2
import psycopg2.extras
# from psycopg2.extras import Json
# from psycopg2.extensions import AsIs
# import re
import json
import credentials

'''
DATABASE_URL = os.environ.get('DATABASE_URL')
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token_key = os.environ.get('access_token_key')
access_token_secret = os.environ.get('access_token_secret')
password = os.environ.get('Password')
user = os.environ.get('User')
dbname = os.environ.get('Database')'''


user_info = {
    'user_id': None,
    'user_name': None,
    'screenname': None,
    'user_loc': None,
    'user_desc': None,
    'user_source': None,
    'verified': None,
    'followers_count': None,
    'friends_count': None,
    'listed_count': None,
    'favourites_count': None,
    'statuses_count': None
}


tweet_info = {
    'user_id': None,
    'tweet_id': None,
    'text': None,
    'source': None,
    'created_at': None,
    'hashtags': None

}


class TwitterClient():
    def __init__(self, twitter_user):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        self.num_tweets = num_tweets
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        print(tweets)
        return tweets

    '''def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(friend_list)

        return friend_list'''

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

# this class will authenticate twitter api and set's call options


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token_key, credentials.access_token_secret)
        return auth
        print('Authenticated')

# This class will authenticate twitter


class twitter_streamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    print('authenticated')

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentication and the connection to the twitter API
        auth = self.twitter_authenticator.authenticate_twitter_app()
        listener = twitter_listener(fetched_tweets_filename)
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

# this class is for streaming and processing live tweets


class twitter_listener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a', encoding='utf-8', errors='ignore') as ex:
                ex.write(data)
                print(type(data))  # --> string
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

# This is a listener class that just prints received tweets


class cleaners():
    def __init__(self, raw_tweets_filename):
        self.raw_tweets_filename = raw_tweets_filename

    def loading(self):
        try:
            with open(self.raw_tweets_filename, 'r') as f:
                data = json.load(f)
            return data
            #print(data.values())
        except BaseException:
            print("error")

    def load_tweet_data():
        try:
            f=open('testfile.json')
            data = json.load(f)  # <- len is 1
            for item in data['tweets']:
                tweet_info['user_id'] = item['user']['id']
                tweet_info['tweet_id'] = item['id']
                tweet_info['text'] = item['text']
                tweet_info['source'] = item['source']
                tweet_info['created_at'] = item['created_at']
                tweet_info['hashtags'] = item['entities']['hashtags']
                Result = tweet_info # <- dict
        except BaseException:
            print('error')
        return list(Result.values()) # <- prints each iterated dict value set

    def tweet_value_set(load_tweet_data):
        tweet_values = load_tweet_data
        candor_list.append(tweet_values)
        print(candor_list)

    def load_user_data():
        try:
            f=open('testfile.json')
            data = json.load(f)
            for item in data['tweets']:
                user_info['user_id'] = item['user']['id']
                user_info['user_name'] = item['user']['name']
                user_info['screenname'] = item['user']['screen_name']
                user_info['user_desc'] = item['user']['description']
                user_info['user_loc'] = item['user']['location']
                user_info['user_source'] = item['source']
                user_info['verified'] = item['user']['verified']
                user_info['followers_count'] = item['user']['followers_count']
                user_info['friends_count'] = item['user']['friends_count']
                user_info['listed_count'] = item['user']['listed_count']
                user_info['favourites_count'] = item['user']['favourites_count']
                user_info['statuses_count'] = item['user']['statuses_count']
                Result = user_info
                #print(list(Result.values()))
        except BaseException:
            print('error')
        return list(Result.values())

    '''def formatting(self):
        try:
            format_data = json.dumps(f, separators=(',', ': '))
        return data

            print(data)'''

# Functionality for analyzing and categorizing content from tweets.


class DatabaseConnection():
    def __init__(self):
        try:
            conn_string = "host='localhost' dbname='suppliers' user='danboser' port='5432'"
            # this can be removed once heroku is in use
            self.conn = pg2.connect(conn_string)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            #self.formatted_tweets_filename = formatted_tweets_filename
            print('Database Connected.')
        except BaseException:
            print('Cannot connect to database')
            # --> to be used when Heroku is involved (DATABASE_URL, sslmode='require')

    def insert_tweet_data(self):
        candor = cleaners.load_tweet_data()
        #print(candor)
        self.cursor.execute("INSERT INTO tweet_info VALUES (%s, %s, %s, %s, %s, %s)", (candor))

    def insert_user_data(self):
        candor = cleaners.load_user_data()
        #print(candor)
        self.cursor.execute("INSERT INTO user_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (candor))

    def closer(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    # hash_tag_list = input("Supply hashtags here. Use quotes, and comma's to delineate:  ")
    # ['poor people', 'war on the poor', 'socio-economics']
    fetched_tweets_filename = "testfile.json"
    raw_tweets_filename = 'testfile.json'
    #raw_tweets_filename = 'tweets2.json'
    formatted_tweets_filename = 'testfile.json'
    #twitter_user = input('Supply Twitter User Name: ')
    #num_tweets = int(input('integer: '))

    #TwitterName = TwitterClient(twitter_user)
    #twitter_client = TwitterName.get_user_timeline_tweets(num_tweets)
    database_connection = DatabaseConnection()
    #clean = cleaners.loading()
    # CreateTable = database_connection.create_table()
    #load = cleaners.load_tweet_data()
    load2 = cleaners.tweet_value_set()
    #insert = database_connection.insert_tweet_data()
    #insert_two = database_connection.insert_user_data()
    # twitter_listener(StreamListener).on_data()
    # streamer = twitter_streamer()
    # streamer_fun = streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
