import email_interface
from spotify_interface import get_token
import time

#print(get_token('nareshr100', scope='user-read-currently-playing,user-read-playback-state,user-top-read,user-modify-playback-state,user-read-private,user-read-email,user-library-read,playlist-modify-public,playlist-modify-private'))

while True:

    email_interface.main(token=get_token('nareshr100', scope='user-read-currently-playing,user-read-playback-state,user-top-read,user-modify-playback-state,user-read-private,user-read-email,user-library-read,playlist-modify-public,playlist-modify-private'))
    time.sleep(15)