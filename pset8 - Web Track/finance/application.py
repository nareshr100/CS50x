import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    assets = db.execute("SELECT * FROM assets WHERE user_id=:user_id",
                user_id = session['user_id'])

    user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session['user_id'])

    total = user_cash[0]['cash']

    i = 0

    for asset in assets:

        symbol = str(assets[i]['stock'])
        volume = int(assets[i]['volume'])
        details = lookup(symbol)
        price = details['price']
        assets[i]['price'] = price
        share_total = price * volume
        assets[i]['share_total'] = share_total
        total += share_total
        i+=1

    return render_template('index.html', assets=assets,
            cash=usd(user_cash[0]['cash']), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    """Buy shares of stock"""
    if request.method == "POST":

        # ensure stock symbol and volume provided
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        if not request.form.get("shares"):
            return apology("Please enter the volume of stock you would like to purchase", 403)

        # get user_id
        user_id = session["user_id"]

        if user_id == None:
            return apology("huh", 401)

        # store symbol
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        # look up Stock price and get volume requested
        details = lookup(symbol)

        if details == None:
            return apology("this stock does not exist", 403)

        volume = request.form.get("shares")
        cost = details['price'] * float(volume)
        name = details['name']
        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)

        if len(user_cash) != 1:
            return apology("database error", 406)

        elif cost > user_cash[0]['cash']:
            return apology("you do not have enough cash to purchase these stocks", 403)

        db.execute("INSERT INTO transactions (user_id, stock, cost, volume) VALUES (?, ?, ?, ?)",
                    (user_id, details['symbol'], cost, volume))

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

        # update user's cash
        db.execute("UPDATE users SET cash=:cash WHERE id=:user_id",
                        cash = user_cash[0]['cash'] - cost, user_id = user_id)
        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT * FROM transactions WHERE user_id=:user_id ORDER BY time DESC;",
                                user_id=session['user_id'])
    print(transactions)

    for transaction in transactions:

        symbol = transaction['stock']
        details = lookup(symbol)
        transaction['name'] = details['name']
        transaction['price'] = details['price']

    return render_template('history.html', transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        # store symbol
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        # look up Stock price
        details = lookup(symbol)

        if details == None:
            return apology("this stock does not exist", 403)

        return render_template("quoted.html", name=details['name'], symbol=details['symbol'], price=details['price'])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirmation password was submitted
        elif not request.form.get("password"):
            return apology("must provide confirmation of password", 403)

        # Ensure username is unique by querying database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        password1 = request.form.get("password")
        password2 = request.form.get("confirm password")

        if len(rows) != 0:
            return apology("username has already been taken, please choose a new one", 403)

        # Ensure password and confirmed password match
        elif (password1 != password2):
            return apology("passwords do not match", 403)

        elif len(password1) < 6 and any(map(str.isdigit, password1)) == False:
            return apology("password requires at least 6 characters and must include a number", 403)

        # input user into database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(password1))
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":

        # get user_id
        user_id = session["user_id"]

        if user_id == None:
            return apology("huh", 401)

        # store symbol
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        if symbol == None:
            return apology("please select a stock to sell", 403)

        # look up Stock price and get volume requested + owned
        details = lookup(symbol)
        volume = int(request.form.get("shares"))
        volume_owned = db.execute("SELECT volume FROM assets WHERE user_id=:user_id AND stock=:stock",
                                    user_id=session['user_id'], stock=symbol)

        if len(volume_owned) != 1:
            return apology("database error", 403)

        volume_owned = int(volume_owned[0]['volume'])
        print(volume_owned)

        if details == None:
            return apology("this stock does not exist", 403)

        elif volume_owned == None or volume_owned == 0:
            return apology("you do not own any shares of this stock", 403)

        elif volume_owned < volume:
            return apology("you do not own that many shares of this stock", 403)

        # update transactions
        cost = -details['price'] * volume
        db.execute("INSERT INTO transactions (user_id, stock, cost, volume) VALUES (?, ?, ?, ?)",
                    (user_id, details['symbol'], cost, -volume))

        # update assets
        if volume_owned - volume == 0:
            db.execute("DELETE FROM assets WHERE user_id=:user_id AND stock=:symbol;",
                        user_id = user_id, symbol = details['symbol'])

        else:
            db.execute("UPDATE assets SET volume=:volume WHERE user_id=:user_id AND stock=:symbol",
                        volume = int(volume_owned) - int(volume), user_id = user_id, symbol = details['symbol'])

        # update user's cash
        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)
        db.execute("UPDATE users SET cash=:cash WHERE id=:user_id",
                    cash = user_cash[0]['cash'] - cost, user_id = user_id)

        return redirect("/")

    else:
        assets = db.execute("SELECT stock FROM assets WHERE user_id=:user_id",
                            user_id = session['user_id'])

        return render_template("sell.html", assets=assets)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
