import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for
# redirect and url_for can be used to call different routes, ex: redirect(url_for('home'))

# create the app
app = flask.Flask(__name__)
# idk what this does
app.config["DEBUG"] = True


# home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    # temporary
    return render_template('home.html')


# register for account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if GET, return a html form for user to sign up
    # if POST, save user information in DB and return a redirect to login\home page

    # POST if user presses submit, before they press submit its a GET request
    return render_template() # remove later


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if GET, return a html form for user to log in
    # if POST, check if entered information is valid/is in the DB
        # if yes, redirect to home page
        # if no, display error message but don't redirect or return anything, user stays on login page

    return render_template() # remove later


# browse all items
@app.route('/browse', methods=['GET'])
def browseAll():
    # Load all items from DB, then pass to browse.html file to display?
    return render_template() #temporary


@app.route('/users',methods=['GET'])
def sampleQuery1():
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()
