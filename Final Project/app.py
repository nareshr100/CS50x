import sqlite3
from flask import Flask, render_template, redirect, request, session, make_response,session,redirect
import spotipy
import spotipy.util as util
import os
import requests
import string

from helpers import query, login_required, apology
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from spotify_interface import *

import email_interface

app = Flask(__name__)

app.secret_key = os.urandom(24)

API_BASE = 'https://accounts.spotify.com'

# Make sure you add this to Redirect URIs in the setting of the application dashboard
CLI_ID = "b98d5c6d61e14ce3b9fde6181ba451f6"
CLI_SEC = "16a41ee8fbc245d28bbfddda248c5508"
REDIRECT_URI= "http://127.0.0.1:5000/api_callback"
SCOPE = 'user-read-currently-playing,user-read-playback-state,user-top-read,user-modify-playback-state,user-read-private,user-read-email,user-library-read,playlist-modify-public,playlist-modify-private'
position = 0
LOGIN = False

# Set this to True for testing but you probably want it set to False in production.
SHOW_DIALOG = True

# authorization-code-flow Step 1. Have your application request authorization; 
# the user logs in and authorizes access
@app.route("/")
def verify():
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    return redirect(auth_url)

@app.route("/index", methods=["GET", "POST"])
def index():

    global position

    email_interface.main(token=session['token'])

    if request.method == "POST":
        
        # get top artists/tracks data
        time_range = request.form.get('time-range')
        if time_range == 'Short Term':
            time_range = 'short_term'

        elif time_range == 'Medium Term':
            time_range = 'medium_term'
            
        else:
            time_range = 'long_term'

        top_tracks_dict = get_top_tracks(token=session['token'], time_range=time_range)
        top_artists_dict = get_top_artists(token=session['token'], time_range=time_range)
        playback_dict = get_current_playback(token=session['token'])

        # implement skip track feature
        if request.form.get('skip') == 'Previous Track' and position != 0:
            previous_track(token=session['token'])
            position -= 1

        elif request.form.get('skip') == 'Next Track':
            next_track(token=session['token'])
            position += 1

        return render_template("index.html", playback=playback_dict, top_tracks=top_tracks_dict, top_artists=top_artists_dict, time_range=request.form.get('time-range'))

    else:

        time_range = 'medium_term'
        top_tracks_dict = get_top_tracks(token=session['token'], time_range=time_range)
        top_artists_dict = get_top_artists(token=session['token'], time_range=time_range)
        playback_dict = get_current_playback(token=session['token'])

        global LOGIN
        if LOGIN == False:

            # check if user in database, if not add to db
            profile_dict = get_profile(token=session['token'])

            try:
                connection = sqlite3.connect("spotitrack.db")
                crsr = connection.cursor() # cursor
            except:
                return print("Could not connect to database")

            crsr.execute("SELECT * FROM users WHERE username=?", (profile_dict['username'],))
            rows = crsr.fetchall()

            if len(rows) == 0: # if no user with this username add to db
                crsr.execute("INSERT INTO users (username, email, product, followers, country) VALUES (?, ?, ?)", 
                            (profile_dict['username'], profile_dict['email'], profile_dict['product'], profile_dict['followers'], profile_dict['country'],))
            
            elif len(rows) == 1: # if one user update user info in case of changes
                crsr.execute("UPDATE users SET email=?, product=?, followers=?, country=? WHERE username=?",
                            (profile_dict['email'], profile_dict['product'], profile_dict['followers'], profile_dict['country'], profile_dict['username'],))

            LOGIN = True

        return render_template("index.html", position=position, playback=playback_dict, top_tracks=top_tracks_dict, top_artists=top_artists_dict, time_range='Medium Term')

# authorization-code-flow Step 2.
# Have your application request refresh and access tokens;
# Spotify returns access and refresh tokens
@app.route("/api_callback")
def api_callback():
    session.clear()
    code = request.args.get('code')

    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:5000/api_callback",
        "client_id":CLI_ID,
        "client_secret":CLI_SEC
        })

    res_body = res.json()
    session["token"] = res_body.get("access_token")

    return redirect("index")


# authorization-code-flow Step 3.
# Use the access token to access the Spotify Web API;
# Spotify returns requested data
@app.route("/go", methods=['POST'])
def go():
    data = request.form    
    return render_template("results.html", data=data)

@app.route("/emails", methods=["GET", "POST"])
def emails():
    """Display information about emails received"""
    
    if request.method == "POST":

        try:
            connection = sqlite3.connect("spotitrack.db")
            crsr = connection.cursor() # cursor
        except:
            return print("Could not connect to database")

        profile_dict = get_profile(token=session['token'])
   

        if request.form.getlist('toggle1') == ['on']:
            crsr.execute("UPDATE users SET notifications = 'Y' WHERE username=?", (profile_dict['username'],))        
        else:
            crsr.execute("UPDATE users SET notifications = 'N' WHERE username=?", (profile_dict['username'],))  
        
        connection.commit()
        connection.close()

    
    return render_template("emails.html")

@app.route("/recommended", methods=["GET", "POST"])
def recommended():
    """Display users recommended songs and artists"""

    seed_artists = None
    seed_tracks = None

    if request.method == "POST":
        
        seed = request.form.get('seed')

        if len(seed) == 0:
            seed_artists=['spotify:artist:1nzgtKYFckznkcVMR3Gg4z']

        elif seed.startswith('spotify:artist'):
            seed_artists=[str(seed)]

        elif seed.startswith('spotify:track'):
            seed_tracks=[str(seed)]
        
        rec_dict = get_recommendations(token=session['token'], seed_artists=seed_artists, seed_tracks=seed_tracks)
        return render_template("recommended.html", rec_dict=rec_dict)

    else:

        seed_artists=['spotify:artist:1nzgtKYFckznkcVMR3Gg4z']
    
        rec_dict = get_recommendations(token=session['token'], seed_artists=seed_artists, seed_tracks=seed_tracks)
        return render_template("recommended.html", rec_dict=rec_dict)

@app.route("/statistics", methods=["GET", "POST"])
def statistics():
    """Display users usage statistics"""

    features_dict = {}
    features_dict_single_track = {}
    track_name = ''

    try:
        connection = sqlite3.connect("spotitrack.db")
        crsr = connection.cursor() # cursor
    except:
        return print("Could not connect to database")
    
    profile_dict = get_profile(token=session['token'])

    crsr.execute("SELECT *FROM user_library_data WHERE user_id=? AND type=?", (profile_dict['username'], 'track',))
    rows = crsr.fetchall()

    library_len = len(rows)

    if request.method == "POST":

        if request.form.get('load') == '1':

            saved_tracks_dict = get_all_saved_tracks(token=session['token'])
            artists_dict = get_artists_from_tracks(token=session['token'], track_dict=saved_tracks_dict)

            try:
                connection = sqlite3.connect("spotitrack.db")
                crsr = connection.cursor() # cursor
            except:
                return print("Could not connect to database")

            profile_dict = get_profile(token=session['token'])

            crsr.execute("DELETE FROM user_library_data WHERE user_id=? AND (type=? OR type=?)", (profile_dict['username'], 'track', 'artist',))        
            
            for item in saved_tracks_dict.items():

                crsr.execute("INSERT INTO user_library_data (user_id, type, uri, name) VALUES (?, ?, ?, ?)",
                            (profile_dict['username'], 'track', item[0], item[1],))
            
            for item in artists_dict.items():

                crsr.execute("INSERT INTO user_library_data (user_id, type, uri, name) VALUES (?, ?, ?, ?)",
                            (profile_dict['username'], 'artist', item[0], item[1],))

        
            connection.commit()
            connection.close()

        if request.form.get('analyse') == '1':

            try:
                connection = sqlite3.connect("spotitrack.db")
                crsr = connection.cursor() # cursor
            except:
                return print("Could not connect to database")
            
            profile_dict = get_profile(token=session['token'])

            crsr.execute("SELECT feature, value FROM user_library_features WHERE user_id=? AND name=?", (profile_dict['username'], 'saved_tracks',))
            rows = crsr.fetchall()

            if len(rows) == 11:

                for row in rows:

                    feature = row[0]
                    value = row[1]

                    if feature != 'tempo' and feature != 'loudness':
                        value = str(round(value*100, 1)) + ' / 100'
                    elif feature == 'loudness':
                        value = str(round(value, 2)) + ' dB'
                    else:
                        value = str(round(value, 1)) + ' BPM'

                    features_dict[str(feature).capitalize()] = value

            else:
                crsr.execute("SELECT uri, name FROM user_library_data WHERE user_id=? AND type=?", (profile_dict['username'], 'track',))
                track_list = crsr.fetchall()
                track_dict = {}
                
                for track in track_list:
                    track_dict[str(track[0])] = str(track[1])

                features_dict_sql = get_all_average_audio_features(token=session['token'], track_dict=track_dict)
                
                for feature in features_dict_sql:
                    crsr.execute("INSERT INTO user_library_features (user_id, name, feature, value) VALUES (?, ?, ?, ?)", 
                                (profile_dict['username'], 'saved_tracks', str(feature), str(features_dict[str(feature)])))

            connection.commit()
            connection.close()

        if request.form.get('go') == '1':

            try:
                connection = sqlite3.connect("spotitrack.db")
                crsr = connection.cursor() # cursor
            except:
                return print("Could not connect to database")
            
            profile_dict = get_profile(token=session['token'])

            crsr.execute("SELECT feature, value FROM user_library_features WHERE user_id=? AND name=?", (profile_dict['username'], 'saved_tracks',))
            rows = crsr.fetchall()

            if len(rows) == 11:

                for row in rows:

                    feature = row[0]
                    value = row[1]

                    if feature != 'tempo' and feature != 'loudness':
                        value = str(round(value*100, 1)) + ' / 100'
                    elif feature == 'loudness':
                        value = str(round(value, 2)) + ' dB'
                    else:
                        value = str(round(value, 1)) + ' BPM'

                    features_dict[str(feature).capitalize()] = value

            connection.commit()
            connection.close()

            track_dict_single = {}
            track_uri = request.form.get('track_uri')
            track_name = get_track_name(token=session['token'], track_uri=str(track_uri))
            track_dict_single[str(track_uri)] = str(track_name)
            features_dict_single = get_all_average_audio_features(token=session['token'], track_dict=track_dict_single)
            features_dict_single_track = {}

            for feature in features_dict_single.items():

                ftr = feature[0]
                value = feature[1]

                if ftr != 'tempo' and ftr != 'loudness':
                    value = str(round(value*100, 1)) + ' / 100'
                elif ftr == 'loudness':
                    value = str(round(value, 2)) + ' dB'
                else:
                    value = str(round(value, 1)) + ' BPM'

                features_dict_single_track[str(ftr).capitalize()] = value

    
    else:

        try:
            connection = sqlite3.connect("spotitrack.db")
            crsr = connection.cursor() # cursor
        except:
            return print("Could not connect to database")
        
        profile_dict = get_profile(token=session['token'])

        crsr.execute("SELECT feature, value FROM user_library_features WHERE user_id=? AND name=?", (profile_dict['username'], 'saved_tracks',))
        rows = crsr.fetchall()

        if len(rows) == 11:

            for row in rows:

                feature = row[0]
                value = row[1]

                if feature != 'tempo' and feature != 'loudness':
                    value = str(round(value*100, 1)) + ' / 100'
                elif feature == 'loudness':
                    value = str(round(value, 2)) + ' dB'
                else:
                    value = str(round(value, 1)) + ' BPM'

                features_dict[str(feature).capitalize()] = value

        connection.commit()
        connection.close()

    return render_template("statistics.html", library_len=library_len, features_dict=features_dict, features_dict_single_track=features_dict_single_track, track_name=track_name) 


if __name__ == "__main__":
    app.run(debug=True)