import spotipy
import sys
from email_interface import send_email
from spotify_interface import get_new_music, get_saved_tracks, add_track_to_playlist

spotify = spotipy.Spotify()

if sys.version_info < (3,0):
    import tkinter as tk
else:
    import tkinter as tk

root = tk.Tk()
root.title("SpotifyApp")
tk.Button(root, text = "SpotifyApp").pack()
tk.mainloop()

