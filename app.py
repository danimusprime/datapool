import tweepy
import psycopg2

# Tweepy API doc here: http://pythonhosted.org/tweepy/html/api.html
# psycopg2 API doc here: http://initd.org/psycopg/docs/

# Keys
  consumer_key = "process.env.consumer_key",
  consumer_secret: "process.env.consumer_secret",
  access_token_key: "process.env.access_token_key",
  access_token_secret: "process.env.access_token_secret"

# Twitter initialization
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth)

# Postgresql initialization
try:
    connection = psycopg2.connect(
        database= 'process.env.DATABASE'
        host= 'process.env.HOST'
        port= 'process.env.PORT'
        user= 'process.env.USER'
        password= 'process.env.PASSWORD')
            print "connected"
                except:
            print "unable to connect"

cursor = connection.cursor()

# The table schema: CREATE TABLE tweets (id SERIAL PRIMARY KEY, tweet_id BIGINT NOT NULL, text VARCHAR NOT NULL, screen_name VARCHAR NOT NULL, author_id INTEGER, created_at VARCHAR NOT NULL, inserted_at TIMESTAMP NOT NULL)

try:
    statuses = api.list_timeline(api.me(@batenkaitos).screen_name, '<NAME OF TIMELINE?>')
    for s in statuses:
        # To remove duplicate entries
        # See http://initd.org/psycopg/docs/faq.html for "not all arguments converted during string formatting"
        cursor.execute("SELECT id FROM tweets WHERE text = %s;", [s.text])
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO tweets (tweet_id, text, screen_name, author_id, created_at, inserted_at) VALUES (%s, %s, %s, %s, %s, current_timestamp);", (s.id, s.text, s.author.screen_name, s.author.id, s.created_at))
            connection.commit()
except tweepy.error.TweepError:
    print "Whoops, could not fetch news!"
except UnicodeEncodeError:
    pass
finally:
    cursor.close()
    connection.close()
