from tweepy.streaming import StreamListener
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Cursor
import psycopg2 as pg2
import os
from pprint import pprint
import credentials


# Keys
# DATABASE_URL = os.environ.get('DATABASE_URL')
# consumer_key = os.environ.get('consumer_key')
# consumer_secret = os.environ.get('consumer_secret')
# access_token_key = os.environ.get('access_token_key')
# access_token_secret = os.environ.get('access_token_secret')
# password = os.environ.get('Password')
# user = os.environ.get('User')
# dbname = os.environ.get('Database')

# this class will authenticate twitter, and
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
        auth.set_access_token(credentials.access_token_key, credentials.access_token_secret)
        return auth


class twitter_streamer():
    '''
    class for streaming and processing live tweets
    '''

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles twitter authentication and the connection to the twitter API
        listener = twitter_listener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)


class twitter_listener(StreamListener):
    '''
    This is a listener class that just prints received tweets
    '''

    def init(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    hash_tag_list = ['poor people', 'war on the poor', 'socio-economics']
    fetched_tweets_filename = "tweets.csv"

    streamer = twitter_streamer()
    streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)


'''
class Database_connection:
    def __init__(self):
        try:
            self.conn = pg2.connect(DATABASE_URL, sslmode='require')
            self.conn.autocommit = True
            self.cursor = self.conn.cursor
        except:
            pprint('Cannot connect to database')

    def create_table(self):
        create_table_command = 'CREATE TABLE tweets(
            id SERIAL PRIMARY KEY,
            tweet_id BIGINT NOT NULL,
            text VARCHAR NOT NULL,
            screen_name VARCHAR NOT NULL,
            author_id INTEGER,
            created_at VARCHAR NOT NULL,
            inserted_at TIMESTAMP NOT NULL)'
        self.cursor.execute(create_table_command)

    def insert_new_record(self):
        new_record = on_data
        insert_command = "INSERT INTO tweets(id, tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES ('" + \
            new_record[0]+"','" + new_record[1] + "')"
        pprint(insert_command)
        self.curor.execute(insert_command)

    def query_all(self):
        self.cursor.execute('SELECT * FROM tweets')
        tweets = self.cursor.fetchall()
        for punk in tweets:
            pprint('Each punk : {0}'.format(punk))


class tweepy_connection:
    lookup(self):
        statuses = api.statuses_lookup(
            id_=14903018, include_entities=False, trim_user=False, map_=False)
    for s in statuses:
        print(s.id, s.text, s.author.screen_name, s.author.id, s.created_at)
        # previous try return self._statuses_lookup(list_to_csv(id_=14903018), include_entities
        # cursor.execute("SELECT id FROM tweets WHERE text = %s;", [s.text])
        # if cursor.rowcount == 0:
        cursor.execute("INSERT INTO tweets (tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, current_timestamp);",
                       (s.id, s.text, s.author.screen_name, s.author.id, s.created_at))
        conn.commit()


except tweepy.error.TweepError:
    print('Whoops, could not fetch news!')
except UnicodeEncodeError:
    pass
finally:
    cursor.close()
    conn.close()


Old data
# host= 'ec2-54-227-241-179.compute-1.amazonaws.com',
# dbname= 'dbname',
# port= '5432',
# user= 'user',
# password= 'password')
'''
