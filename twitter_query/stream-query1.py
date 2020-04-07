import tweepy
from tweepy import OAuthHandler, Stream, StreamListener


consumer_key = 'nHAKpd3UWAWmHI63gkq2IcwKu'
consumer_secret = 'Z532JvyGCZwaWP8ZDQQOknjWLqX7mcUTWsNeSNCcFadT4MlNAr'
access_token_key = '302604042-nx3SJxEaUdNkvbB9oNAZyKHohjOENULQm5rZfnbi'
access_token_secret = 'TvBfFe850haSeIAiDGgcEAUx8TXCyEMVhDBxUZXFQYgeh'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print("Auth successful via", api.me().name)
print("Getting the stream... ctrl+c to stop any time.")

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('query_04052020.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

#Set the hashtag to be searched
twitter_stream = Stream(auth, MyListener())

# https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter
#track - Keywords to track. Phrases of keywords are specified by a comma-separated list. See track for more information.
twitter_stream.filter(track=['ICU beds',
                             'ppe',
                             'masks',
                             'long hours',
                             'deaths',
                             'hospitalized',
                             'cases',
                            'ventilators',
                            'respiratory',
                            'hospitals',
                            '#covid',
                            '#coronavirus'])
