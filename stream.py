import threading
import tweepy
import json
import sys


def extract_tweet(message):
    try:
        tweet = json.loads(str(message))
    except ValueError, e:
        return None

    # Sometimes we just get back spurious data, like integers and stuff
    if not isinstance(tweet, dict):
        return None

    return tweet

def extract_lat_lon(tweet):
    """
    Searches for the lat and lon and returns it.
    """
    _coords = {'lat':None, 'lon':None}
    geo = tweet.get('geo')
    if geo:
        geo_type = geo.get('type')
        if geo_type.lower() != 'point':
            return _coords

        lat, lon = geo.get('coordinates')
    else:
        place = tweet.get('place')
        if not place:
            return _coords

        bounding_box = place.get('bounding_box')
        if not bounding_box:
            return _coords

        coords = bounding_box.get('coordinates')
        if not coords:
            return _coords

        lat, lon = coords[0][0]

    if lat and lon:
        _coords = {'lat':lat, 'lon':lon}

    return _coords


class Listener(tweepy.StreamListener):
    def __init__(self, *args, **kwargs):
        self.stream_callback = lambda m: m
        if 'stream_callback' in kwargs:
            self.stream_callback = kwargs['stream_callback']
            del kwargs['stream_callback']
        super(Listener, self).__init__(*args, **kwargs)

    def on_data(self, data):
        if data: # don't worry about blank lines
            self.stream_callback(data)

def run_thread(consumer_key, consumer_secret,
               access_token, access_token_secret, ts):

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        streaming_api = tweepy.streaming.Stream(auth,
                                                Listener(
                                                    stream_callback=
                                                    ts.handle_message
                                                ),
                                                timeout=60)
        # Geo box that covers the entire earth to ensure we only get
        # geo-located tweets.
        streaming_api.filter(locations=[-180, -90, 180, 90])
    except KeyboardInterrupt:
        sys.exit()



class TwitterStream(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token, access_token_secret):
        self.clients = {}
        threading.Thread(target=run_thread, args=(
            consumer_key, consumer_secret,
            access_token, access_token_secret, self)).start()

    def add_client(self, client):
        self.clients[client.uuid] = client

    def remove_client(self, client):
        del self.clients[client.uuid]

    def handle_message(self, message):
        tweet = extract_tweet(message)
        coords = extract_lat_lon(tweet)

        for uuid, client in self.clients.items():
            client.write_message({
                'geo': coords,
                'tweet': tweet,
            })


