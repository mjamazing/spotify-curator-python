# Client credentials access - Alternate Method
# credentials = oauth2.SpotifyClientCredentials(
#         client_id='',
#         client_secret=''
#         )
# token = credentials.get_access_token()
# sp = spotipy.Spotify(auth=token)

# Client credentials access - Preferred Method
# client_credentials_manager = SpotifyClientCredentials(client_id='', client_secret='')
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

