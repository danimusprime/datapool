import tweepy
import psycopg2 as pg2
import os
from pprint import pprint
import credentials

# Tweepy API doc here: http://pythonhosted.org/tweepy/html/api.html
# psycopg2 API doc here: http://initd.org/psycopg/docs/

# Keys
# DATABASE_URL = os.environ.get('DATABASE_URL')
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token_key = os.environ.get('access_token_key')
access_token_secret = os.environ.get('access_token_secret')
# password = os.environ.get('Password')
# user = os.environ.get('User')
# dbname = os.environ.get('Database')


class tweepy_connection(tweepy.StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == "__main__":

    listener = tweepy_connection()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    stream = tweepy.Stream(auth, listener)

    stream.filter(track=['poor people', 'war on the poor', 'socio-economics'])

    # api = tweepy.API(auth)


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
