import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pprint
import sys
import ConfigParser
import ast

config = ConfigParser.SafeConfigParser()
config.read('config.ini')

def track_lookup(artist_name, track_name):
  results = sp.search(q='track:' + track_name, type='track', limit=50)
  for i, track in enumerate(results['tracks']['items']):
    for j, artist in enumerate(track['artists']):
      if artist_name == artist['name'].encode('ascii', 'ignore') and track_name == track['name'].encode('ascii', 'ignore'):
        return track['id']
  return ''

def artist_lookup(artist_name):
  results = sp.search(q='artist:' + artist_name, type='artist')
  for i, artist in enumerate(results['artists']['items']):
    if artist_name == artist['name'].encode('ascii', 'ignore'):
      return artist['id']
  return ''

username = config.get('USER','USERNAME')

# Authorization Code Flow
token = util.prompt_for_user_token(username, scope=config.get('AUTHORIZATION','SCOPE'), client_id=config.get('AUTHORIZATION','CLIENT_ID'), client_secret=config.get('AUTHORIZATION','CLIENT_SECRET'), redirect_uri=config.get('AUTHORIZATION','REDIRECT_URI'))
sp = spotipy.Spotify(auth=token)

# Get config variables
playlist_name = config.get('PLAYLIST', 'PLAYLIST_NAME')
artist_seed_ids = list(map(lambda x: artist_lookup(x), config.get('PLAYLIST', 'ARTIST_SEEDS').split('|')))
track_seed_ids = list(map(lambda x: track_lookup(*x.split('>')), config.get('PLAYLIST', 'TRACK_SEEDS').split('|')))
genre_seeds = list(config.get('PLAYLIST', 'GENRE_SEEDS').split('|'))
playlist_settings = ast.literal_eval(config.get('PLAYLIST', 'PLAYLIST_SETTINGS'))

# Loop through user's playlists to find if it exists
playlist_id = ""
results = sp.current_user_playlists(limit=50)
for i, item in enumerate(results['items']):
  if playlist_name == item['name'].encode('ascii', 'ignore'):
    playlist_id = item['id']

# If playlist doesn't exist, create it
if playlist_id == "":
  playlist_id = sp.user_playlist_create(username, playlist_name, public = False)['id']

# Get tracks based on seeds
track_recommendation_ids = []
track_recommendations = sp.recommendations(seed_artists=artist_seed_ids, seed_genres=genre_seeds, seed_tracks=track_seed_ids, limit=100, country="US", **playlist_settings)
for track in track_recommendations["tracks"]:
  track_recommendation_ids.append(track["id"])

# Add the song results to the playlist
results = sp.user_playlist_replace_tracks(username, playlist_id, track_recommendation_ids)