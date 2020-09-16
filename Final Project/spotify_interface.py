'''
------------------------------

Set up interface with Spotify

------------------------------

'''

import spotipy
import sys
import spotipy.util as util
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import timeit
import time
import string
import sqlite3

spotify = spotipy.Spotify()

def get_token(username, scope=None, client_id='b98d5c6d61e14ce3b9fde6181ba451f6', client_secret='16a41ee8fbc245d28bbfddda248c5508', redirect_uri='https://open.spotify.com/'):

    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    return token

def get_top_tracks(token, limit=20, offset=0, time_range='medium_term'):

    top_tracks_dict = {}
    sp = spotipy.Spotify(auth=token)
    tracks = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)

    for track in tracks['items']:
        top_tracks_dict[track['uri']] = track['name']

    return top_tracks_dict

def get_top_artists(token, limit=20, offset=0, time_range='medium_term'):

    top_artists_dict = {}
    sp = spotipy.Spotify(auth=token)
    artists = sp.current_user_top_artists(limit=limit, offset=offset, time_range=time_range)

    for artist in artists['items']:
        top_artists_dict[artist['uri']] = artist['name']

    return top_artists_dict

def get_current_playback(token):

    sp = spotipy.Spotify(auth=token)
    playback = sp.current_playback()

    if playback == None:
        return None

    playback_dict = {}

    playback_dict['track'] = playback['item']['name']
    playback_dict['uri'] = playback['item']['uri']

    artists = playback['item']['artists']
    artist_list = []

    for artist in artists:
        artist_list.append(artist['name'])


    playback_dict['artists'] = artist_list


    return playback_dict


def previous_track(token):

    sp = spotipy.Spotify(auth=token)
    sp.previous_track()

    return

def next_track(token):

    sp = spotipy.Spotify(auth=token)
    sp.next_track()

    return

def get_saved_tracks(token, limit, dic=True, offset=0):

    # create dictionary to store track name and track_id (uri)
    saved_tracks_dict = {}
    saved_tracks_list = []
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)

    for item in results['items']:

        track = item['track']

        if dic == True:
            saved_tracks_dict[track['uri']] = track['name']
        else:
            saved_tracks_list.append([track['uri'], track['name']])
    
    if dic == True:
        return saved_tracks_dict
    else:
        return saved_tracks_list

def get_all_saved_tracks(token, dic=True):

    saved_tracks_dict = {}
    saved_tracks_list = []
    offset = 0

    while offset <= 10000:
        print(offset)

        if dic == True:
            tracks_dict = get_saved_tracks(token=token, limit=50, dic=True, offset=offset)
            if len(tracks_dict) == 0:
                break
            saved_tracks_dict = {**saved_tracks_dict, **tracks_dict}
            offset += 50
            
        else:
            tracks_list = get_saved_tracks(token=token, limit=50, dic=False, offset=offset)
            if len(tracks_list) == 0:
                break
            saved_tracks_list.append(tracks_list)
            offset += 50

    if dic == True:
        return saved_tracks_dict
    else:
        return saved_tracks_list
    

'''def get_users_playlists(username, SPOTIPY_CLIENT_ID ="b98d5c6d61e14ce3b9fde6181ba451f6", SPOTIPY_CLIENT_SECRET="16a41ee8fbc245d28bbfddda248c5508"):

    client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlists = sp.user_playlists(username,limit=20, offset=0)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None'''

def get_recommendations(token, seed_artists=None, seed_genres=None, seed_tracks=None):

    sp = spotipy.Spotify(auth=token)
    results = sp.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks)
    rec_tracks_dict = {}

    for item in results['tracks']:
        rec_tracks_dict[item['uri']] = item['name']

    return rec_tracks_dict

def get_audio_features(token, track_id):

    sp = spotipy.Spotify(auth=token)
    results = sp.audio_features(track_id)

    return results

def get_average_audio_feature(token, track_dict, feature):

    feature_list = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    avg_feature = 0
    
    if feature not in feature_list:
        ValueError("Feature does not exist")
    elif type(track_dict) != dict:
        TypeError('Tracks must be a dict containing track ids')
    elif type(token) != str:
        TypeError('token must be a string')

    for track in track_dict:
        audio_features = get_audio_features(token=token, track_id=track)
        avg_feature += audio_features[0][str(feature)]
        print(avg_feature)

    avg_feature /= len(track_dict)

    return avg_feature

def get_all_average_audio_features(token, track_dict):

    l = len(track_dict)
    print("l = " + str(l))
    avg_features_dict = {'danceability':0, 'energy':0, 'key':0, 'loudness':0, 'mode':0, 'speechiness':0, 'acousticness':0, 'instrumentalness':0, 'liveness':0, 'valence':0, 'tempo':0}

    if type(track_dict) != dict:
        TypeError('Tracks must be a dict containing track ids')
    elif type(token) != str:
        TypeError('token must be a string')

    i = 0

    for track in track_dict:
        audio_features = get_audio_features(token=token, track_id=track)

        for feature in avg_features_dict:
            avg_features_dict[str(feature)] += audio_features[0][str(feature)]
        
        if i % 100 == 0:
            print(i)

        i += 1
    
    for feature in avg_features_dict:
        avg_features_dict[str(feature)] /= l

    return avg_features_dict

def get_profile(token):

    sp = spotipy.Spotify(auth=token)
    profile = sp.me()
    profile_dict = {}
    profile_dict['username'] = profile['id']
    profile_dict['email'] = profile['email']
    profile_dict['product'] = profile['product']
    profile_dict['followers'] = profile['followers']['total']
    profile_dict['country'] = profile['country']

    return profile_dict

def get_artists_from_tracks(token, track_dict):

    sp = spotipy.Spotify(auth=token)

    artist_dict = {}
    uri_list = []
    counter = 1

    for track in track_dict:

        #track_uri = track
        track_uri = track.lstrip('spotify:track.')

        if counter % 50 == 0:
            uri_list.append(track_uri)
            results = sp.tracks(uri_list)

            for track in results['tracks']:

                for artist in track['artists']:
                    artist_dict[artist['uri']] = artist['name']

            print(counter)
            uri_list = []

        else:
            uri_list.append(track_uri)

        counter += 1  
    
    return artist_dict

def get_new_music(token):

    sp = spotipy.Spotify(auth=token)
    results = sp.new_releases(limit=50)

    new_music_dict = {}

    for item in results['albums']['items']:
        artist_names = []
        artist_uris = []

        for artist in item['artists']:
            artist_names.append(artist['name'])
            artist_uris.append(artist['uri'])

        new_music_dict[item['uri']] = [item['name'], item['release_date'], artist_uris, artist_names]
    
    return new_music_dict

def get_new_relevant_music(token):

    profile_dict = get_profile(token=token)

    try:
        connection = sqlite3.connect("spotitrack.db")
        crsr = connection.cursor() # cursor
    except:
        return print("Could not connect to database")

    crsr.execute("SELECT uri FROM user_library_data WHERE user_id=? AND type=?", (profile_dict['username'], 'artist',))
    artists = crsr.fetchall()

    artists_list = []

    for artist in artists:
        artists_list.append(artist[0])

    all_new_music_dict = get_new_music(token=token)
    rel_new_music_dict = {}

    for item in all_new_music_dict.items():

        if item[1][1] == datetime.today().strftime('%Y-%m-%d'):

            for i in range(len(item[1][2])):

                if item[1][2][i] in artists_list:
                    rel_new_music_dict[str(item[0])] = item[1]
                    break
    
    connection.close()

    return rel_new_music_dict

def create_playlist(token, user_id):

    reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
    reqBody = {'name': 'SpotiTracker', 'description': 'New releases tailored to your tastes thanks to SpotiTracker!', 'public': 'true'}
    requests.post('https://api.spotify.com/v1/users/{}/playlists'.format(user_id), headers=reqHeader, json=reqBody)
    
    return

def upload_playlist_image(playlist_id, image_b64='spotitracker.jpeg'):

    img = open(image_b64)
    print(img)
    sp = spotipy.Spotify(auth=token)
    sp.playlist_upload_cover_image(playlist_id=playlist_id, image_b64=img)

    return


def get_users_playlists(token, user_id):

    reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
    r = requests.get('https://api.spotify.com/v1/users/{}/playlists'.format(user_id), headers=reqHeader)
    results = r.json()

    return  results 

def update_new_tracks_playlist(token, new_music_dict, playlist_uri):

    if len(new_music_dict) == 0:
        return print('no new music today')

    else:
        sp = spotipy.Spotify(auth=token)
        
        playlist_id = playlist_uri.lstrip('spotify:playlist.')

        for item in new_music_dict.items():
            tracks_list = []
            tracks = sp.album_tracks(item[0])

            for track in tracks['items']:
                tracks_list.append(track['uri'])

            reqHeader = {'Authorization': 'Bearer {}'.format(token), 'Content-Type': 'application/json'}
            reqBody = {'uris': tracks_list}
            requests.post('https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id), headers=reqHeader, json=reqBody)

    return

def get_track_name(token, track_uri):

    sp = spotipy.Spotify(auth=token)
    track = sp.track(track_uri)
    track_name = track['name']
    return track_name


token = 'BQC0dpLS927eaKwe7-GH6Cty4GjoIiwEWTmDUGhH022SYSTPChnJNZcOQU2Z49RHxzdmnL_R8V9342MHv7ghjlsmNLrTt5wGAj7YL-2NaOuhxc3sFc8B4CPOcbtNItm6czpOBFZnduqXKVMhUpGYqE9hPZuLHTaaw4Fwu6x929fev2kZbkhKcvLPfwDLN8M4f-K2Uk-9P4inJ2Mb6JyYD529Gf9jGWwvuYjQrfXQn-tjoB3F67v4VXRxrfkxKSpSG9f16oTWI0r67Tjr'

#saved = get_all_saved_tracks(token=token, dic=True)
#artist_dict = get_artists_from_tracks(token=token, track_dict=saved)
#new_music_dict = get_new_relevant_music(token=token)
#print(get_new_relevant_music(token=token))

#update_new_tracks_playlist(token=token, new_music_dict=new_music_dict, playlist_uri='spotify:playlist:6AIdaisySdebXaHtaTqO0l')

#print(get_users_playlists(token=token, user_id='nareshr100'))

#upload_playlist_image(playlist_id='4Jm7D3isRvJghYreGGvGVq')
#print(get_track_name(token=token, track_uri='spotify:track:5ry2OE6R2zPQFDO85XkgRb'))