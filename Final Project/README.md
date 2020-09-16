SPOTITRACKER

SpotiTracker is a web-based flask application that utilises the Spotify API functionality through a python library, Spotipy.

To use this application you must have a spotify account with an associated email address.You will be asked to authenticate the webpage via Spotify before it can be used hence this requirement!

Open the files in an IDE and in the terminal execute 'flask run' to begin the application.

The homepage contains a list of your top 20 tracks and top 20 artists, set to a medium time range as default. 
This can be changed via the dropdown and by hitting 'Go'. When music is playing on one of your devices through your Spotify acccount, the song you are playing and the artists in the song will be displayed. In addition to this there are 'Next Track' and 'Previous Track' buttons that skips through songs that you are playing. When you close the Spotify app and stop any Spotify activity this will disappear.

The 'emails' page shows your email notifications settings which you can change via a toggle switch and then by pressing 'Save' to save your preferences. SpotiTracker will send an email notification whenever new music is released from artists you like. This is defined as any artist who appears in one or more songs that you have 'liked' on Spotify. This can be turned off as aforementioned and emails are sent to the email address associated with your Spotify account automatically.

The 'recommendations' page initially shows 20 recommended tracks based on a random artist in your liked artists. There is an option to enter a Spotify track or artist 'URI' (Uniform Resource Identifier) to generate recommendations based off that artist or track. The URI of an artist or track can be optained through spotify under the 'share' feature on a track or artist. Each time the page is reloaded or 'Go' is pressed new recommendations will be generated.

The 'statistics' tab displays the number of liked songs you have in your library. If your library hasn't been loaded this will not be displayed. To load your library, click the 'Load' button and wait approximately one minute (usually less). You can then analyse every song in your library to get average audio features such as how danceable, energetic and what average tempo your music is at. You can also analyse an individual track by entering a track URI into the search bar and then pressing 'Go'. This will return the audio features of this particular track.

This completes the features of my web application!