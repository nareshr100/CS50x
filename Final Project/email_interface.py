'''
----------------------------------------

Set up secure email interface using SMTP

----------------------------------------

'''

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from spotify_interface import get_new_relevant_music, get_profile, update_new_tracks_playlist, create_playlist, get_users_playlists

import sqlite3
import string
import time

#token = 'BQB4W1nfvk7RguiFVQaho9z5iAg_0Ee9BkV8GU__wetylyfJnDbqR30OrnLqEzewJ11j74hrHGmoAIBnwAUTxxJ_u3MLGiEcW-1Oc7opOtBd9Uvz5dmsdjMy86Bxj9qA8aLYHGq_oZ-2dJ9NwMfVAVLYGFrC2BaDkxWjm5sF1Cs89NFg7-psStlwt9EKG8I6SnVElkXptZxOE2lD4AjSAHLA20yu3SpGw-cSQFKV2sAUe2bm68ETE404n0d2lqDrYsbMt3Uzbf9gqQQH'

check = False

def main(token):

    global check 
    t = time.localtime()
    current_time = time.strftime("%H:%M", t)

    if (current_time == '00:00' or current_time == '05:30') and check == False:
        
        check = True
        profile_dict = get_profile(token=token)

        try:
            connection = sqlite3.connect("spotitrack.db")
            crsr = connection.cursor() # cursor
        except:
            return print("Could not connect to database")

        crsr.execute("SELECT email, notifications FROM users WHERE username=?", (profile_dict['username'],))
        rows = crsr.fetchall()

        email = rows[0][0]

        if rows[0][1] == 'Y':

            new_music_dict = get_new_relevant_music(token=token)

            if len(new_music_dict) == 0:
                return print('no new music today')

            else:
                crsr.execute("SELECT uri FROM user_library_data WHERE user_id=? AND type=?", (profile_dict['username'], 'playlist'))
                rows1 = crsr.fetchall()

                if len(rows1) == 0:
                    playlist_uri = None
                    create_playlist(token=token, user_id=profile_dict['username'])
                    results = get_users_playlists(token=token, user_id=profile_dict['username'])

                    for item in results['items']:

                        if item['name'] == 'SpotiTracker':

                            playlist_uri = item['uri']
                            name = item['name']
                            break
                    
                    crsr.execute("INSERT INTO user_library_data (user_id, type, uri, name) VALUES (?, ?, ?, ?)", (profile_dict['username'], 'playlist', playlist_uri, name,))

                else: 
                    playlist_uri = rows[0][0]
                    print(playlist_uri)

                subject, mail_content = generate_mail_content(token=token, new_music_dict=new_music_dict, notif_type="new_music")
                update_new_tracks_playlist(token=token, new_music_dict=new_music_dict, playlist_uri=playlist_uri)
                
                connection.commit()
                connection.close()
                
                return send_mail(str(email), subject=subject, mail_content=mail_content)

        else:
            return print('user has notifications turned off')

    elif (current_time == '00:01' or current_time == '05:31'):
        check = False
    

def generate_mail_content(token, new_music_dict, notif_type):

    profile_dict = get_profile(token=token)

    start = 'Hello ' + str(profile_dict['username']) + ',\n\n'
    end = 'Thank you for using SpotiTracker!'
    subject = 'SpotiTracker Email Notification'

    if notif_type == "new_music":
        middle = "We have newly released music that you may like! Check out the tracks below by copying the URI into Spotify's search bar and give them a listen. You can unsubscribe from this notification service at any time from the emails tab on our site. Alternatively, view the SpotiTrcaker playlist that will be in your library to view all new tracks!\n\n\n\n"
        
        new_releases = ''

        for track in new_music_dict.items():

            artists = ''

            for i in range(len(track[1][2])):
                
                if i != len(track[1][2]) - 1:
                    artists = artists + str(track[1][3][i]) + ', '
                else:
                    artists = artists + str(track[1][3][i])

            new_releases = new_releases + "name: " + str(track[1][0]) + "\nURI: " + str(track[0]) + "\nRelease Date: " +  str(track[1][1]) + "\nArtists: " +  artists + '\n\n'

        new_releases = new_releases + '\n\n'
        mail_content = start + middle + new_releases + end

    else:
        middle = 'ERROR\n\n'
        mail_content = start + middle + end

    return subject, mail_content



def send_mail(recipient, subject, mail_content):

    if type(recipient) != str:
        TypeError("recipient email address must be of a string format")

    #The mail addresses and password
    sender_address = 'spotitracker@gmail.com'
    sender_pass = 'spotitracker100'
    receiver_address = recipient

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = 'SpotiTracker'
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    try:
        session.sendmail(sender_address, receiver_address, text)
    except:
        return print('error')
    
    session.quit()
    return print('Mail Sent')
