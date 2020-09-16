'''
------------------------------

Set up interface with Spotify

------------------------------

'''

import spotipy
import sys
import spotipy.util as util
from classes import artist
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import date
import timeit

spotify = spotipy.Spotify()

SPOTIPY_CLIENT_ID ="b98d5c6d61e14ce3b9fde6181ba451f6"
SPOTIPY_CLIENT_SECRET="16a41ee8fbc245d28bbfddda248c5508"

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)

    return result

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)

    return z

def get_token(username, scope=None, client_id='b98d5c6d61e14ce3b9fde6181ba451f6', client_secret='16a41ee8fbc245d28bbfddda248c5508', redirect_uri='https://open.spotify.com/'):

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return token

def get_saved_tracks(username, limit, offset=0):

    #create token to access data
    token = get_token(username, scope='user-library-read')

    #create dictionary to store track name and track_id (uri)
    saved_tracks_dict = {}

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks(limit, offset)
        for item in results['items']:
            track = item['track']
            saved_tracks_dict[track['name']] = track['uri']
        
    else:
        print("Can't get token for", username)

    return saved_tracks_dict

def get_new_music_by_country(country=None, limit=20, offset=0):

    albums = spotify.new_releases(country)

    return albums

'''def get_new_music_by_artist(artist_id, country='GB'):

    token = get_token('nareshr100')
    spotify = spotipy.Spotify(auth=token)
    songs = spotify.artist_top_tracks(artist_id, country)
    

    for track in songs:
        date = songs['tracks'][0]['album']['release_date']

        if date 
       

    tracks = 
    return tracks'''

D_Block_Europe = artist('spotify:artist:5VadK1havLhK1OpKYsXv9y', 'D Block Europe', 'Trap', '5')


def get_users_playlists(username, SPOTIPY_CLIENT_ID ="b98d5c6d61e14ce3b9fde6181ba451f6", SPOTIPY_CLIENT_SECRET="16a41ee8fbc245d28bbfddda248c5508"):

    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists(username,limit=20, offset=0)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None


def add_track_to_playlist(username, playlist_id, tracks, position=None):

    #get token to authorise modification of playlist with correct scope
    token = get_token(username, scope='playlist-modify-private')
    
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_add_tracks(username, playlist_id , tracks, position)

def get_artists_from_track(username, track_id):
    
    token = get_token(username, scope='user-library-read')
    #artist = None

    if token:
        sp = spotipy.Spotify(auth=token)
        result = sp.track(track_id)
        artists = result['artists']
        artists_dict = {}
        

        for i in range(len(artists)):

            key = artists[i]['name']
            value = artists[i]['uri']
            artists_dict[key] = value

    else:
        print("Can't get token for", username)
    
    return artists_dict

def get_artists_from_saved_tracks(username):

    saved_tracks_dict = {}
    artists_dict = {}
   
    for i in range(100):
        x = get_saved_tracks(username, limit=20, offset=(20*i))
        saved_tracks_dict = merge_two_dicts(saved_tracks_dict, x)

    for track in saved_tracks_dict:
        x = get_artists_from_track(username, saved_tracks_dict[track])
        artists_dict = merge_two_dicts(artists_dict, x)

    return saved_tracks_dict


tracks = ['spotify:track:6XNANAB7sFvkfho6bMCp7o'] #Summertime in Paris - Jaden
playlist_id = 'spotify:playlist:6AIdaisySdebXaHtaTqO0l' #New Tunes - python.
#add_track_to_playlist(username='nareshr100', playlist_id=playlist_id, songs=songs)

#print(get_saved_tracks(username='nareshr100', limit=10, offset=0))

code_to_test = '''
saved_tracks_dict = {}

   
for i in range(100):
    x = get_saved_tracks(username='nareshr100', limit=20, offset=(20*i))
    saved_tracks_dict = merge_two_dicts(saved_tracks_dict, x)


'''

#elapsed_time = timeit.timeit(code_to_test, number=1)
#print(elapsed_time)

#print(get_artists_from_saved_tracks(username='nareshr100'))
'''x={'a': 'a', 'b': 'b'}
y={'c':'c'}
print(merge_two_dicts(x, y))'''

#print(get_artists_from_track(username='nareshr100', track_id = 'spotify:track:16oi4OiKmkO51l60F5R9kR'))

'''token = get_token('nareshr100')
spotify = spotipy.Spotify(auth=token)
songs = spotify.artist_top_tracks(artist_id='2hlmm7s2ICUX0LVIhVFlZQ', country="GB")
album = songs['tracks'][0]['album']
date = album['release_date']
print(date)'''



today = date.today()
#print("Today's date:", today)

#print(get_users_playlists('dhanyarasa100'))

def trial(username, SPOTIPY_CLIENT_ID ="b98d5c6d61e14ce3b9fde6181ba451f6", SPOTIPY_CLIENT_SECRET="16a41ee8fbc245d28bbfddda248c5508"):

    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    tracks = sp.current_user_saved_tracks(limit=5, offset=0)

    return tracks

#print(trial('dhanyarasa100'))

#add_track_to_playlist('nareshr100', 'spotify:playlist:6AIdaisySdebXaHtaTqO0l', tracks

token = get_token('dhanyarasa100', scope='playlist-modify-private')
    
sp = spotipy.Spotify(auth=token)

print(sp.current_user())