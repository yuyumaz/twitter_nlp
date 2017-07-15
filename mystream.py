import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json 

def convert_valid(one_char): 
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars: 
        return one_char
    else: 
        return '_'

class MyListener(StreamListener): 
    def __init__(self, data_dir, query): 
        query_fname = ''.join(convert_valid(one_char) for one_char in query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data): 
        try: 
            with open(self.outfile, 'a') as f: 
                if json.loads(data)['lang'] == 'en': f.write(data)
                return True
        except BaseException as e: 
            print("error on data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status): 
        print(status)
        return True 
        
if __name__ == '__main__': 
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

    query = input("Please enter a keyword to track: ")
    new_dir = input("Please enter the directory you would like to store it in: ")

    twitter_stream = Stream(auth, MyListener(new_dir, query))
    twitter_stream.filter(track=query)

