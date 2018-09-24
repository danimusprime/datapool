import tweepy
import psycopg2 as pg2
import os

# Tweepy API doc here: http://pythonhosted.org/tweepy/html/api.html
# psycopg2 API doc here: http://initd.org/psycopg/docs/

# Keys
DATABASE_URL= os.environ.get('DATABASE_URL')
consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token_key = os.environ.get('access_token_key')
access_token_secret = os.environ.get('access_token_secret')
password= os.environ.get('Password')
user= os.environ.get('User')
dbname= os.environ.get('Database')

# Twitter initialization
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# Postgresql initialization
conn = pg2.connect(DATABASE_URL, sslmode='require')
    #host= 'ec2-54-227-241-179.compute-1.amazonaws.com',
    #dbname= 'dbname',
    #port= '5432',
    #user= 'user',
    #password= 'password')
print (('status is: ') + str(conn.status))

cursor = conn.cursor()

#CREATE TABLE tweets (id SERIAL PRIMARY KEY, tweet_id BIGINT NOT NULL, text VARCHAR NOT NULL, screen_name VARCHAR NOT NULL, author_id INTEGER, created_at VARCHAR NOT NULL, inserted_at TIMESTAMP NOT NULL)

try:
    statuses = tweepy.cursor(API.statuses_lookup, id=14903018)
    #for status in statuses.items(200):
        # To remove duplicate entries
        # See http://initd.org/psycopg/docs/faq.html for "not all arguments converted during string formatting"
    cursor.execute("SELECT id FROM tweets WHERE text = %s;", [s.text])
    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO tweets (tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, current_timestamp);", (s.id, s.text, s.author.screen_name, s.author.id, s.created_at))
        conn.commit()
except tweepy.error.TweepError:
    print ('Whoops, could not fetch news!')
except UnicodeEncodeError:
    pass
finally:
    cursor.close()
    conn.close()
