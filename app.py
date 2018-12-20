from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Cursor
# import dataset
import psycopg2 as pg2
# import os
from pprint import pprint
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
dbname = os.environ.get('Database')
'''


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit=True)

        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(tweet)
        return friend_list

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

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentication and the connection to the twitter API
        listener = twitter_listener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

# this class is for streaming and processing live tweets


class twitter_listener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
                print(type(data))  # --> string
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
        '''
    def data_insert(self):
        try:
            with open(self.fetched_tweets_filename) as tf:
                source = tf.read()
                data = json.loads(source)
            for item in data['user']:

            return True
        except BaseException:
            print(item)
        return True
        '''

    def on_error(self, status):
        print(status)

# This is a listener class that just prints received tweets


class DatabaseConnection:
    def __init__(self):
        try:
            conn_string = "host='localhost' dbname='suppliers' user='danboser' port='5432'"
            # this can be removed once heroku is in use
            self.conn = pg2.connect(conn_string)
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            pprint('Database Connected.')
        except BaseException:
            pprint('Cannot connect to database')
            # --> to be used when Heroku is involved (DATABASE_URL, sslmode='require')

    def create_table(self):
        create_table_command = "CREATE TABLE twitter(id SERIAL PRIMARY KEY, tweet_id BIGINT NOT NULL, screen_name VARCHAR NOT NULL, text_  VARCHAR NOT NULL, full_text VARCHAR NOT NULL, favorite_count INTEGER, quote_count INTEGER, reply_count INTEGER, retweet_count INTEGER, location VARCHAR NULL, url VARCHAR NULL, description VARCHAR NULL, source VARCHAR NOT NULL, author_id INTEGER, created_at VARCHAR NOT NULL, inserted_at TIMESTAMP NOT NULL)"
        self.cursor.execute(create_table_command)
        pprint('Table Created')

    def insert_new_record(self):
        try:
            # with open(tweets.json) as f:
            # new_record = json.load(f)
            # for item in new_record[]:
            insert_command = 'INSERT INTO twitter(id, text, screen_name, tweet_id, full_text, favorite_count, retweet_count, reply_count, quote_count, location, url, description, source, created_at, inserted_at) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp)'
            self.cursor.execute(insert_command, (id, text, screen_name, tweet_id, full_text, favorite_count,
                                                 retweet_count, reply_count, quote_count, location, url, description, source, created_at, inserted_at))
            self.cursor.commit()
            pprint('Data Inserted.')
        except BaseException:
            pprint('Error.')

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":

    hash_tag_list = ['poor people', 'war on the poor', 'socio-economics']
    fetched_tweets_filename = "tweets.json"

    # database_connection = DatabaseConnection()
    # twitter_listener(StreamListener).on_data()
    # CreateTable = database_connection.create_table()
    # insert_record = database_connection.insert_new_record()
    # twitter_client = TwitterClient('Batenkaitos')
    # twitterClient = twitter_client.get_user_timeline_tweets(6)
    streamer = twitter_streamer()
    streamer_fun = streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

'''
    tweet_id = item['id']
    screen_name = item['user']['screen_name']
    text = item['text']
    full_text = item['user']['extended_tweet']['full_text']
    favorite_count = item['user']['extended_tweet']['entities']['favorite_count']
    quote_count = item['user']['extended_tweet']['entities']['quote_count']
    reply_count = item['user']['extended_tweet']['entities']['reply_count']
    retweet_count = item['user']['extended_tweet']['entities']['retweet_count']
    location = item['user']['location']
    url = item['user']['url']
    description = item['user']['description']
    source = item['source']
    created_at = item['created_at']
    inserted_at = TIMESTAMP(item['inserted_at']
'''
