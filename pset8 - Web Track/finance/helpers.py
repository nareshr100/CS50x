import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

"""def trade(stock, volume, deal):

    # get user_id
    user_id = session["user_id"]

    if user_id == None:
        return apology("huh", 401)

    # store symbol
    symbol = stock
    symbol = symbol.upper()

    # look up Stock price and get volume requested
    details = lookup(symbol)

    if details == None:
        return apology("this stock does not exist", 403)

    volume = volume
    cost = details['price'] * float(volume)
    volume_owned = db.execute("SELECT volume FROM assets WHERE user_id=:user_id AND stock=:stock",
                                user_id=session['user_id'], stock=symbol)

    if len(volume_owned) != 1:
        return apology("database error", 403)

    volume_owned = int(volume_owned[0]['volume'])

    if deal == 'sell':
        cost = -cost

    name = details['name']
    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)

    if len(user_cash) != 1:
        return apology("database error", 406)

    elif deal == 'buy' and cost > user_cash[0]['cash']:
        return apology("you do not have enough cash to purchase these stocks", 403)

    db.execute("INSERT INTO transactions (user_id, stock, cost) VALUES (?, ?, ?)",
                (user_id, details['symbol'], cost))

    if deal == 'buy':
        # check if user owns this stock already
        owned = db.execute("SELECT * FROM assets WHERE user_id=:user_id AND stock=:symbol",
                    user_id=user_id, symbol=str(details['symbol']))

        # if unowned create new asset
        if len(owned) == 0:
            db.execute("INSERT INTO assets (user_id, stock, volume, name) VALUES (?, ?, ?, ?)",
                        (user_id, details['symbol'], volume, name))


        # if owned update existing asset
        elif len(owned) == 1:
            db.execute("UPDATE assets SET volume=:volume WHERE user_id=:user_id AND stock=:symbol",
                        volume = int(volume) + int(owned[0]['volume']), user_id = user_id, symbol = details['symbol'])

        else:
            return apology("database error", 406)

    else:
        if volume_owned == None or volume_owned == 0:
            return apology("you do not own any shares of this stock", 403)

        elif volume_owned < volume:
            return apology("you do not own that many shares of this stock", 403)

        # update assets
        elif volume_owned - volume == 0:
            db.execute("DELETE FROM assets WHERE user_id=:user_id AND stock=:symbol;",
                        user_id = user_id, symbol = details['symbol'])

        else:
            db.execute("UPDATE assets SET volume=:volume WHERE user_id=:user_id AND stock=:symbol",
                        volume = int(volume_owned) - int(volume), user_id = user_id, symbol = details['symbol'])

    # update user's cash
    db.execute("UPDATE users SET cash=:cash WHERE id=:user_id",
                    cash = user_cash[0]['cash'] - cost, user_id = user_id)
    return redirect("/")"""