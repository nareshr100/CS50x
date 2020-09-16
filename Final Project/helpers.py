import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

import sqlite3


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def query(query, rw):

    if type(query) != str:
        TypeError('query must be of a string format')

    # Query database for username
    try:
        connection = sqlite3.connect("spotitrack.db")
        crsr = connection.cursor() # cursor
    except:
        return print("Could not connect to database")

    # execute SQL query
    if rw == 'read':
        crsr.execute(query)
        rows = crsr.fetchall()
        connection.close()  # close the connection 
        return rows

    elif rw == 'write':
        crsr.execute(query)
        connection.close()  # close the connection 
    
    return

    

    
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function   