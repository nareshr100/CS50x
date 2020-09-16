import sys

import spotipy
import spotipy.util as util

spotify = spotipy.Spotify()

class artist:

    def __init__(self, artist_id, name, genre, rating):

        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.rating = rating

class song:

    def __init__(self, song_id, name, length, artist):

        self.song_id = song_id
        self.name = name
        self.length = length
        self.artist = artist

class playlist:

    def __init__(self, name,length, genre):
        
        self.name = name
        self.length = length
        self.genre = genre

    
    def add_song_to_playlist(self, song, playlist):

        if len(sys.argv) > 3:
            username = sys.argv[1]
            playlist_id = sys.argv[2]
            track_ids = sys.argv[3:]
        else:
            print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
            sys.exit()

        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(username, scope)

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
            print(results)
        else:
            print("Can't get token for", username)