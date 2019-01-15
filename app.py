from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Cursor
import psycopg2 as pg2
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

    '''def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends).items(num_friends):
            friend_list.append(tweet)
        return friend_list'''

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
                print(data)  # --> string
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

# This is a listener class that just prints received tweets


class data_cleaning():

    def __init__(self, raw_tweets_filename):
        self.raw_tweets_filename = raw_tweets_filename

        with open(self.raw_tweets_filename, 'r') as f:
            data = json.load(f, strict=False)

        with open('format.json', 'w') as test:
            formatted_data = json.dump(data, test, ensure_ascii=False, indent=2)

        for item in formatted_data['tweets']:
            created_at = item['created_at']
            tweet_id = item['id']
            text = item['extended_tweet']['full_text']
            quotes = item['quote_count']
            reply_count = item['reply_count']
            retweet_count = item['retweet_count']
            user_name = item['user']['name']
            screen_name = item['user']['screen_name']
            user_id = item['user']['id']
            user_loc = item['user']['location']
            user_desc = item['user']['description']
            hashtags = item['entities']['hashtags']


# This class loads the data in proper JSON format for use to brdige the DICT POSTGRES gap


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
        create_table_command = "CREATE TABLE twitter(id SERIAL PRIMARY KEY, created_at VARCHAR, tweet_id BIGINT NOT NULL, text  VARCHAR NOT NULL, quotes INT, reply_count INT, retweet_count INT, user_name VARCHAR,  screen_name VARCHAR NOT NULL, user_id INTEGER, user_loc VARCHAR, user_desc VARCHAR, hashtags VARCHAR);"
        self.cursor.execute(create_table_command)
        pprint('Table Created')

    def insert_new_record(self):
        with open('tweets.json', 'r') as f:
            data = json.load(f, strict=False)
            for item in data['tweets']:
                created_at = item['created_at']
                tweet_id = item['id']
                text = item['extended_tweet']['full_text']
                quotes = item['quote_count']
                reply_count = item['reply_count']
                retweet_count = item['retweet_count']
                user_name = item['user']['name']
                screen_name = item['user']['screen_name']
                user_id = item['user']['id']
                user_loc = item['user']['location']
                user_desc = item['user']['description']
                hashtags = item['entities']['hashtags']
                insert_command = "INSERT INTO twitter (created_at, tweet_id, text, quotes, reply_count, retweet_count, user_name, screen_name, user_id, user_loc, user_desc, hashtags) VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s,)", (
                    created_at, tweet_id, text, quotes, reply_count, retweet_count, user_name, screen_name, user_id, user_loc, user_desc, hashtags)
                self.cursor.execute(insert_command, data,)
                self.cursor.commit()
                pprint('Data Inserted.')

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":

    hash_tag_list = ['poor people', 'war on the poor', 'socio-economics']
    fetched_tweets_filename = "tweets.json"
    raw_tweets_filename = 'tweets.json'
    formated_tweets_filename = 'format.json'

    database_connection = DatabaseConnection()
    # CreateTable = database_connection.create_table()
    insert = database_connection.insert_new_record()
    # twitter_listener(StreamListener).on_data()
    # twitter_client = TwitterClient('Batenkaitos')
    # twitterClient = twitter_client.get_user_timeline_tweets(6)
    # clean = data_cleaning(raw_tweets_filename)
    # key streamer = twitter_streamer()
    # key streamer_fun = streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
